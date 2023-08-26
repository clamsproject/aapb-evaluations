# Tesseract OCR Evaluation Report

## App

The `preds` MMIF files were generated using the [Tesseract OCR Wrapper](http://apps.clams.ai/tesseractocr-wrapper/v1.0/). Annotations were generated on bounding boxes created through the [East Text Detection](http://apps.clams.ai/east-textdetection/v1.1/) app.

## Evaluation Dataset

The gold annotation data can be found [here]().

## Evaluation Code

The script used for evaluation can be found [here](https://github.com/clamsproject/aapb-evaluations/blob/eaed0134ae6609dc3b5fda8ff45fc9ebea403eef/ocr_eval/evaluate.py).

## Metrics

This dataset was evaluated using `Character Error Rate` , or `CER`. CER is a measurement of the accuracy of the predictions - it is the proportion of *incorrectly* predicted characters, calculated using edit distance. Edit distance can be thought of as *"the least number of operations required to convert one string to another, where an operation can be one of substitution, deletion or insertion."*

As such, a higher CER represents a more inaccurate prediction, with perfect prediction being 0.0. Ideal CER performance is around the 10-20% range (0.1-0.2)

### Aggregation

CER was calculated on a document level. Since the metric is simple and between [0,1], we aggregate the CER across all documents by means of simple averaging.

### Results

| Filename               |  CER      |
|------------------------|-----------|
|cpb-aacip-507-bz6154fc44|  0.8678   |
|cpb-aacip-507-cf9j38m509|  0.8603   |
|cpb-aacip-507-zw18k75z4h|  0.9815   |
|cpb-aacip-507-pc2t43js98|  0.9524   |
|cpb-aacip-525-9g5gb1zh9b|  0.9031   |
|cpb-aacip-507-n29p26qt59|  0.9872   |
|cpb-aacip-507-nk3610wp6s|  0.9026   |
|cpb-aacip-507-7659c6sk7z|  0.8912   |
|cpb-aacip-507-vd6nz81n6r|  0 (empty)|
|cpb-aacip-525-bg2h70914g|  0.8892   |
|cpb-aacip-507-4t6f18t178|  0.9485   |
|cpb-aacip-507-6w96689725|  1.0      |
|cpb-aacip-507-zk55d8pd1h|  1.0      |
|cpb-aacip-525-028pc2v94s|  0.9398   |
|cpb-aacip-507-v40js9j432|  1.0      |
|cpb-aacip-507-m61bk17f5g|  0.8753   |
|cpb-aacip-507-pr7mp4wf25|  0.9427   |
|cpb-aacip-507-vm42r3pt6h|  0.8831   |
|cpb-aacip-507-9882j68s35|  1.0      |
|cpb-aacip-525-3b5w66b279|  0.9568   |
|cpb-aacip-507-v11vd6pz5w|  0.8235   |
|cpb-aacip-507-r785h7cp0z|  0.9387   |
|cpb-aacip-507-154dn40c26|  0.9807   |
| **Average**              |**0.8924** |

### Side-by-Side Views

The side-by-side comparison of gold and test annotations is visible within the [`results` output](https://github.com/clamsproject/aapb-evaluations/blob/eaed0134ae6609dc3b5fda8ff45fc9ebea403eef/ocr_eval/results@tesseractocr-wrapper1.0@batch2).
Each file consists of the annotations for one video document,a which look like the following:

```json
  "300.3003003003003": {
    "gold_text": "sen. pete domenici\\nchairman, budget committee",
    "test_text": "c h a i r m a n ,",
    "cer": 0.8695651888847351
  },
```