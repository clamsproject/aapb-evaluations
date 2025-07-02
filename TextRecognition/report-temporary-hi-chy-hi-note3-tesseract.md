# Evaluation Report for `TextRecognition` task as of 2025-07-02 09:37:54.023558

## Evaluation method
Evaluating Text Recognition (a.k.a OCR) results, using CER (Character 
Error Rate) metric. CER calculates the accuracy on the character level,
using edit distance algorithm. Namely, CER tells "how many edits" it 
takes to correct the predicted result into the gold standard text. That 
said, note that 

1. For CER, the lower the value, the better the performance.
1. CER can be more that 100%, although it sounds strange. 

(When this evaluator could not find any matching pairs between a gold 
and a prediction, it will return -1 for CER values.)
(When this evaluator could not find any predictions at all for a GUID, 
it will return False for CER values.)

General information on TR evaluation can be found https://en.wikipedia.org/wiki/Optical_character_recognition#Accuracy
And more details on the edit distance (Levenshtein algorithm) can be found https://en.wikipedia.org/wiki/Levenshtein_distance

## Data specs
- Groundtruth data location: ../aapb-annotations/understanding-chyrons/golds'
- System prediction (MMIF) location: TextRecognition/preds@app-tesseract-2.0@hi-chy-hi-samples/'

## Pipeline specs

## Raw Results
```
GUID,mean-CER-cased,mean-CER-uncased
cpb-aacip-225-20ftth6f,0.7105263157894737,0.6842105263157895
cpb-aacip-225-65v6x41w,-1,-1
cpb-aacip-225-31qftxh5,-1,-1
cpb-aacip-225-51vdnj5t,0.8737640079103492,0.3922214897824654
cpb-aacip-225-48sbchm7,False,False
cpb-aacip-225-15bcc3x8,1.1511936339522546,1.1511936339522546
cpb-aacip-225-44bnzxh7,-1,-1
cpb-aacip-225-27zkh3tm,-1,-1
cpb-aacip-225-37vmd093,-1,-1
Average,0.9118279858840258,0.7425418833501697

```

## Side-by-side view
<table border="1" class="dataframe table table-striped" id="sbs-table">
  <thead>
    <tr style="text-align: right;">
      <th>guid</th>
      <th>at</th>
      <th>gold</th>
      <th>pred</th>
      <th>cased_cer</th>
      <th>uncased_cer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>360027</td>
      <td>REP. EZRA KANOHO (D)<br><br>Lihue/Kapaa</td>
      <td>< : 4<br><br>Am<br>* ¥<br>REP. EZRA KAMoHO (BD)<br><br>a<br><br></td>
      <td>0.710526</td>
      <td>0.684211</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (4 rows)</td>
      <td>644878</td>
      <td>Sterling Paulos<br><br>Hotel Director<br><br>NCL Hawaii</td>
      <td>AS<br>STERLING PAULOS<br>Hove DiRecroR<br><br>NCL Haw<br><br></td>
      <td>0.585366</td>
      <td>0.243902</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (4 rows)</td>
      <td>954521</td>
      <td>Susan Todani<br><br>Director of Investments<br><br>Kamehameha Schools</td>
      <td>SUSAN TODANI<br><br>DIRECTOR OF InvesTMENTS<br><br></td>
      <td>1.162162</td>
      <td>0.540541</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>245145</td>
      <td>Ted Liu<br><br>Director<br><br>DBEDT</td>
      <td>Y<br><br>ae<br>Te Liv X<br>Director<br>DBEDT<br><br></td>
      <td>0.379310</td>
      <td>0.379310</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>640507</td>
      <td>Mark Sasaki<br><br>Big City Diner</td>
      <td>=<br>a<br>=<br>a<br>=<br>=<br>=<br><br></td>
      <td>1.923077</td>
      <td>1.923077</td>
    </tr>
  </tbody>
</table>