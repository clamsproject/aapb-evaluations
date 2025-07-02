from pathlib import Path
from typing import Any, Union

from clams_utils.aapb import guidhandler
from lapps.discriminators import Uri
from mmif.serialize import Mmif

from common import ClamsAAPBEvaluationTask
from common.metrics import classification_report

"""
Note that this evaluation script is using Brat `.ann` files as gold data, 
but the ann files do not contain the full text. The URL below is the 
location of the source text files used for ann annotation task. (source 
text files are stored in a private repository, due to IP concerns)
"""
GOLD_ANNOTATION = 'https://github.com/clamsproject/aapb-annotations/tree/main/newshour-namedentity'
SRC_UNDER_GOLDS = "https://github.com/clamsproject/aapb-collaboration/tree/89b8b123abbd4a9a67c525cc480173b52e0d05f0/21"

# normalize the labels to be used in the evaluation
label_dict = {'PERSON': 'person', 
              'ORG': 'organization', 
              'FAC': 'location', 
              'GPE': 'location', 
              'LOC': 'location',
              'EVENT': 'event', 
              'PRODUCT': 'product', 
              'WORK_OF_ART': 'program/publication_title',
              'program_title': 'program/publication_title', 
              'publication_title': 'program/publication_title'}
valid_labels = set(list(label_dict.keys()) + list(label_dict.values()))


class NamedEntityRecognitionEvaluator(ClamsAAPBEvaluationTask):
    """
    Evaluating Named Entity Recognition (NER) results, as a sequence 
    labeling task, using precision, recall, and F1 score. The evaluation 
    is done on the token level, meaning the boundary of each entity is
    not taken into account.
    (boundary information usually encoded with B, I, O tagging scheme to 
    indicate "begin", "inside", and "outside" of an entity)

    Here's an example; 
    - gold: "Mark(PER) Zuckerburg(PER)"
    - pred: "Mark(O) Zuckerburg(PER)"
    then 1 miss (FN) and 1 hit (TP)
    
    Considering the fact that in most cases, the majority of the text 
    content is non-entities, non-entities (`O` labels) are not included 
    in the final score board to prevent the score skewed by the large 
    volume of `O` labels.
    """
    
    def __init__(self, batchname: str, gold_loc: Union[str, Path] = None, pred_loc: Union[str, Path] = None, **kwargs):
        super().__init__(batchname, gold_loc, pred_loc)
        self.logger.setLevel('DEBUG')
        self.include_bio = False

    def _read_gold(self, gold_file: Union[str, Path], **kwargs) -> Any:
        """
        gold file is brat ann file, and this will return a list of BIO
        tags. The ann is a tab-separated file with the following format:
        T1	ORG 0 5	Mark
        
        The resulting data should be a dict, where each element represent 
        a token (whitespace-based) with its key being (s,e) int tuple 
        and the value being the NE label 
        """
        tokens = {}
        with (open(gold_file, 'r') as in_f):
            for linenum, line in enumerate(in_f, 1):
                try:
                    _, label, start, final, text = line.split(maxsplit=4)
                except ValueError as e:
                    self.logger.error(line, line.split())
                    raise e
                start = int(start)
                if label in valid_labels:
                    # normalize the label string, otherwise treat it as already normalized
                    if label in label_dict:
                        label = label_dict[label]
                else:
                    raise ValueError(f'invalid label found ({label}) in {gold_file}:{linenum}')
                for tokennum, token in enumerate(text.split()):
                    prefixed_label = label if not self.include_bio \
                        else 'B-' + label if tokennum == 0 else 'I-' + label
                    end = start + len(token)
                    tokens[(start, end)] = prefixed_label
                    start = end + 1
        # at this point, all "positive" tokens from gold annotation are stored in the `tokens` dict
        guid = guidhandler.get_aapb_guid_from(gold_file.name)
        self.logger.debug(f'{guid}, GOLD total positive tokens: {len(tokens)}, first 10: {list(tokens.keys())[:10]}')
        return tokens

    def _read_pred(self, pred_file: Union[str, Path], gold, **kwargs) -> Any:
        """
        The goal here is not only to build a dict of [(start, end) : label]
        (just like the above in the gold reader), but also to insert `O` 
        labels to the gold dict, and finally make sure the numbers of 
        elements in both gold and pred dicts are the same. While doing so, 
        this code tries to fix some errors in the gold annotation. 
        An example of such error is in `cpb-aacip-507-154dn40c26` in 
        `newshour-namedentity` project, where source text 
        "... It's about two Continentals. ..." (ln 335 in the source file)
        and the annotation is only done on "Continental" (not whole token).
        """
        f = open(pred_file, 'r')
        mmif_str = f.read()
        f.close()
        mmif = Mmif(mmif_str)
        token_annotations_id_to_anchor = {ann.id: (mmif.get_start(ann), mmif.get_end(ann)) 
                                          for ann in mmif.get_view_contains(Uri.TOKEN).get_annotations(at_type=Uri.TOKEN)}
        
        pred = {}
        for ne in mmif.get_view_contains(Uri.NE).get_annotations(Uri.NE):
            label = ne.get_property('category')
            if label not in valid_labels:
                # warn about the unknown label 
                # self.logger.warn(f'unknown label found ({label}) in {pred_file}:{ne.id}, ignoring the entity')
                continue
            if 'targets' in ne.properties:
                # meaning NE is anchored on tokens 
                label = label_dict[label]
                for tokennum, target in enumerate(ne.get_property('targets')):
                    s, e = token_annotations_id_to_anchor[target]
                    prefixed_label = label if not self.include_bio \
                        else 'B-' + label if tokennum == 0 else 'I-' + label
                    pred[(s, e)] = prefixed_label
            elif 'start' in ne.properties and 'end' in ne.properties:
                # meaning we're in trouble now since there's no easy way to know about `O` tokens without re-tokenizing 
                # ATM, spacy wrapper always produces token annotations as well and use them as anchors for NE annotations
                # but this an change in to future
                raise ValueError(f'no token annotations found in {pred_file}, hence cannot process `O` tokens')
            
        # at this point, all "positive" tokens from pred mmif is stored in the `pred` dict 
        guid = guidhandler.get_aapb_guid_from(pred_file.name)
        self.logger.debug(f'{guid}, PRED total positive tokens: {len(pred)}, first 10: {list(pred.keys())[:10]}')
        
        # before inserting `O` tokens, do some sanity check and try to fix some obvious errors in annotation 
        # such as "drag-to-select" only part of token
        fixed_gold = {}
        for gold_anchor in gold.keys():
            if gold_anchor not in token_annotations_id_to_anchor.values():
                fixed = False
                for token_anchor in token_annotations_id_to_anchor.values():
                    if gold_anchor[0] == token_anchor[0]:
                        fixed_gold[token_anchor] = gold[gold_anchor]
                        self.logger.debug(f'fixed gold token {gold_anchor} to {token_anchor}')
                        fixed = True
                        break
                if not fixed:
                    raise ValueError(f'gold token {gold_anchor} not found in MMIF tokens')
            else:
                fixed_gold[gold_anchor] = gold[gold_anchor]
        for pa in pred.keys():
            if pa not in token_annotations_id_to_anchor.values():
                raise ValueError(f'pred token {pa} not found in MMIF tokens')
        gold = fixed_gold

        # and finally, insert `O` labels for tokens not positively annotated
        for out_token in token_annotations_id_to_anchor.values():
            if out_token not in pred:
                pred[out_token] = 'O'
            if out_token not in gold:
                gold[out_token] = 'O'
        # at this point, both pred and gold dicts should look like 
        # {(start, end): label} 
        # where "label" values are one of B-X, I-X, O (X can be any of 
        # valid category name defined at the top of the code) but the 
        # elements in both dicts are NOT SORTED by the character offsets.
        # Final sanity check to make sure all character offsets are
        # in there in both gold and pred
        pred_anchors = list(sorted(pred.keys()))
        gold_anchors = list(sorted(gold.keys()))
        if len(pred_anchors) != len(gold_anchors):
            raise ValueError(f'number of tokens in pred and gold do not match in {pred_file}')
        self.logger.debug(f'{guid}, total labels to evaluate: {len(pred_anchors)}')
        for panchor, ganchor in zip(pred_anchors, gold_anchors):
            if panchor != ganchor:
                raise ValueError(f'anchors do not match between gold and pred in {pred_file}')
        return pred, gold
            
    def _compare_pair(self, guid: str, gold: Any, pred: Any) -> Any:
        pred_labels = [pred[key] for key in sorted(pred.keys())]
        gold_labels = [gold[key] for key in sorted(gold.keys())]
        # remove `O` labels from the calculation
        labelset = set(pred_labels + gold_labels)
        labelset.discard('O')
        report = classification_report(gold_labels, pred_labels, labels=list(labelset), output_dict=True)
        return report

    def _compare_all(self, golds, preds) -> Any:
        agg_gold_labels = []
        agg_pred_labels = []
        for gold, pred in zip(golds, preds):
            agg_gold_labels.extend([gold[key] for key in sorted(gold.keys())])
            agg_pred_labels.extend([pred[key] for key in sorted(pred.keys())])
        # remove `O` labels from the calculation
        labelset = set(agg_pred_labels + agg_gold_labels)
        labelset.discard('O')
        report = classification_report(agg_gold_labels, agg_pred_labels, labels=list(labelset), output_dict=False)
        return report

    def _finalize_results(self):
        if len(self._calculations) == 1 and '*' in self._calculations:
            self.results = self._calculations['*']
        else:
            self.results = self._calculations


if __name__ == "__main__":
    parser = NamedEntityRecognitionEvaluator.prep_argparser()
    args = parser.parse_args()

    evaluator = NamedEntityRecognitionEvaluator(args.batchname, args.golds, args.preds)
    evaluator.calculate_metrics(by_guid=False)
    report = evaluator.write_report()
    args.export.write(report.getvalue())
