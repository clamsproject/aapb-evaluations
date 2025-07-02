# Evaluation Report for `TextRecognition` task as of 2025-07-02 09:37:23.635247

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
- System prediction (MMIF) location: TextRecognition/preds@app-doctr-1.3@hi-chy-hi-samples/'

## Pipeline specs

## Raw Results
```
GUID,mean-CER-cased,mean-CER-uncased
cpb-aacip-225-20ftth6f,0.5490707215408646,0.536939389458313
cpb-aacip-225-65v6x41w,0.15263157894736842,0.15263157894736842
cpb-aacip-225-31qftxh5,False,False
cpb-aacip-225-51vdnj5t,0.7333983244250717,0.029192392307146403
cpb-aacip-225-48sbchm7,False,False
cpb-aacip-225-15bcc3x8,0.6916809605488852,0.29073756432247
cpb-aacip-225-44bnzxh7,0.23110367892976588,0.2246934225195095
cpb-aacip-225-27zkh3tm,0.16384068167604754,0.16384068167604754
cpb-aacip-225-37vmd093,0.08824896197614587,0.08572370945089335
Average,0.3728535582920213,0.21196553409739258

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
      <td>202135</td>
      <td>PHIL ESTERMANN<br><br>Save Sandy Beach Coalition</td>
      <td>PHIL<br><br>ESTERMANN<br><br>kpues uontegoougeeg</td>
      <td>0.666667</td>
      <td>0.666667</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>230764</td>
      <td>STEVE HIRANO<br><br>Good Neighbors/Good Planning</td>
      <td>STEVE<br><br>HIRANO<br><br>p090/510qu619N.290 Planning</td>
      <td>0.500000</td>
      <td>0.500000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>248282</td>
      <td>DONNA GOTH<br><br>Land Use Research Foundation<br><br>of Hawaii</td>
      <td>DONNA<br><br>GOTH<br><br>Land Use Researchfoundation<br><br>ofHawail</td>
      <td>0.120000</td>
      <td>0.100000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>321522</td>
      <td>JOANN YUKIMURA (D)<br><br>Kauai Mayor</td>
      <td>NIVOr FENWENA G<br><br>Kauail JokeW</td>
      <td>0.724138</td>
      <td>0.724138</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>360027</td>
      <td>REP. EZRA KANOHO (D)<br><br>Lihue/Kapaa</td>
      <td>-<br><br>A<br><br>A<br><br>EZRA<br><br>KANOHO 6<br><br>eedeyenuin</td>
      <td>0.685714</td>
      <td>0.685714</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>437504</td>
      <td>GOV. JOHN WAIHEE (D)</td>
      <td>Jan. 31<br><br>PAQ5 JOHN WAIHEE(D)</td>
      <td>0.464286</td>
      <td>0.464286</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>494528</td>
      <td>GARY GILL<br><br>Honolulu City Council Member</td>
      <td>GARY<br><br>GILL<br><br>nnjouof Gitycouncil Member<br><br>-</td>
      <td>0.341463</td>
      <td>0.317073</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>532900</td>
      <td>JOHN RADCLIFFE<br><br>Good Neighbors/Good Planning</td>
      <td>NHOF ELETEGVE<br><br>poop/PERENGIYRROD Bupued</td>
      <td>0.948718</td>
      <td>0.871795</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>1021755</td>
      <td>MARTHA HULBERT<br><br>Adoption Circle of Hawaii</td>
      <td>MARTHA<br><br>HULBERT<br><br>tondopy Gircle of Hawail</td>
      <td>0.268293</td>
      <td>0.268293</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (16 rows)</td>
      <td>1308141</td>
      <td>ARTHUR ROSS<br><br>Neighborhood Board Chairman</td>
      <td>ENHEY 3033<br><br>pangapouvequeN Ghatrman</td>
      <td>0.771429</td>
      <td>0.771429</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-65v6x41w (15 rows)</td>
      <td>250150</td>
      <td>CHARLES TOGUCHI<br><br>Superintendent<br><br>Dept. of Education</td>
      <td>CHARLES TOGUCHI<br><br>Superintendent<br><br>Depto of yoneonpa</td>
      <td>0.200000</td>
      <td>0.200000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-65v6x41w (15 rows)</td>
      <td>1179646</td>
      <td>Rep. DANIEL KIHANO</td>
      <td>Rep. DANIEL<br><br>KIHANO</td>
      <td>0.105263</td>
      <td>0.105263</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (4 rows)</td>
      <td>286753</td>
      <td>Connie Lau<br><br>CEO<br><br>American Savings Bank</td>
      <td>CONNIE LAU<br><br>CEO<br><br>AMERICAN SAVINGS BANK</td>
      <td>0.605263</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (4 rows)</td>
      <td>644878</td>
      <td>Sterling Paulos<br><br>Hotel Director<br><br>NCL Hawaii</td>
      <td>STERLING PAULOS<br><br>HOTEL DIRECTOR<br>NCL HAWAIL</td>
      <td>0.690476</td>
      <td>0.047619</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (4 rows)</td>
      <td>954521</td>
      <td>Susan Todani<br><br>Director of Investments<br><br>Kamehameha Schools</td>
      <td>SUSAN TODANI<br>DIRECTOR OF INVESTMENTS<br>KAMEHAMEHA SCHOOLS</td>
      <td>0.818182</td>
      <td>0.036364</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (4 rows)</td>
      <td>1032032</td>
      <td>Rosalind Schurgin<br><br>Executive Vice President<br><br>Festival Companies</td>
      <td>ROSALIND SCHURGIN<br>EXECUTIVE VICE PRESIDENT<br>FESTIVAL COMPANIES</td>
      <td>0.819672</td>
      <td>0.032787</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>245145</td>
      <td>Ted Liu<br><br>Director<br><br>DBEDT</td>
      <td>TED LIU<br>DIRECTOR<br>DBEDT</td>
      <td>0.590909</td>
      <td>0.090909</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>640507</td>
      <td>Mark Sasaki<br><br>Big City Diner</td>
      <td>THE EMPLOYEES STARS<br><br>mam<br><br>MARK SASAKI<br><br>BIG CITY DINER</td>
      <td>0.792453</td>
      <td>0.490566</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (6 rows)</td>
      <td>270904</td>
      <td>JOHN RADCLIFFE<br><br>Former Congressional Candidate</td>
      <td>NHOP RADGLIFFE<br><br>Former Congressional Candidate</td>
      <td>0.108696</td>
      <td>0.108696</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (6 rows)</td>
      <td>347514</td>
      <td>GERRY KEIR<br><br>Managing Editor<br><br>Honolulu Advertiser</td>
      <td>GERRY KER<br><br>a<br><br>u<br><br>Managing Editor<br><br>a Monolokabberitor</td>
      <td>0.384615</td>
      <td>0.365385</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (6 rows)</td>
      <td>830030</td>
      <td>ANDREW POEPOE<br><br>Co-Chairman<br><br>Saiki in '88 Committee</td>
      <td>ANDREW B0d30d<br><br>Co-Chairman,<br><br>Saikiin 88. Committee</td>
      <td>0.200000</td>
      <td>0.200000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (4 rows)</td>
      <td>149016</td>
      <td>WHITNEY ANDERSON (R)<br><br>State Senate Candidate<br><br>District 25 Kailua, Waimanalo</td>
      <td>- I -<br><br>WHITNEY NOSHIONV (R)<br><br>State Senate Candidate<br><br>Distrist 25 Kailua, Waimanalu</td>
      <td>0.182927</td>
      <td>0.182927</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (4 rows)</td>
      <td>312779</td>
      <td>FRED HEMMINGS (R)<br><br>State Senate Candidate<br><br>District 25 Kailua, Waimanalo</td>
      <td>FRED HEMMINGS (R)<br><br>State Senate Candidate<br><br>District SC Kailua, Waimanale</td>
      <td>0.041667</td>
      <td>0.041667</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (4 rows)</td>
      <td>933767</td>
      <td>ALEX SONSON (D)<br><br>State Rep. Candidate<br><br>District 36 Pearl City, Waipahu</td>
      <td>ALEX NOSNOS @<br><br>SIBIS $ Candidate<br><br>District 95 Pearl Chy, Waipainu</td>
      <td>0.323077</td>
      <td>0.323077</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (4 rows)</td>
      <td>985652</td>
      <td>ROY TAKUMI (D)<br><br>State Rep. Candidate<br><br>District 36 Pearl City, Waipahu</td>
      <td>ROYTAKUMI 9<br>State Rep. Candidate<br><br>District 99 Pearl City, Waipahu</td>
      <td>0.107692</td>
      <td>0.107692</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>174775</td>
      <td>Rep. SAMUEL LEE (D)<br><br>Vice Chairman<br><br>House Education Committee</td>
      <td>Rep. SAMUEL LEE (D<br><br>Vice Chairman<br><br>House Education Committee</td>
      <td>0.016667</td>
      <td>0.016667</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>185886</td>
      <td>Sen. BERTRAND<br><br>KOBAYASHI (D)<br><br>Chairman, Senate Education Committee</td>
      <td>ues BERTRAND<br><br>KOBAYASHI<br><br>D)<br><br>Chairman, Senate Education Committee</td>
      <td>0.076923</td>
      <td>0.076923</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>214281</td>
      <td>Rep. ROD TAM (D)<br><br>Chairman<br><br>House Education Committee</td>
      <td>Rep ROD TAM D<br><br>Chairman<br><br>House Education Committee</td>
      <td>0.060000</td>
      <td>0.060000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>255255</td>
      <td>Rep. BOB McEACHERN<br><br>Minnesota Legislator</td>
      <td>Rep.BOB MGEACHERN<br><br>Minnesota<br><br>Legislator</td>
      <td>0.100000</td>
      <td>0.100000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>295529</td>
      <td>Sen. MIKE McCARTNEY (D)<br><br>Vice Chairman<br><br>Senate Education Committee</td>
      <td>Sen. MIKE MCGARTNEY (D)<br><br>Vice Chairman<br><br>Senate Education Committee</td>
      <td>0.030303</td>
      <td>0.015152</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>447648</td>
      <td>EVAN THOMAS<br><br>Common Cause</td>
      <td>BAN THOMAS<br><br>Common Cause</td>
      <td>0.083333</td>
      <td>0.083333</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>461128</td>
      <td>PATSY T. MINK<br><br>The Public Reporter</td>
      <td>PATSY UC MINK<br><br>The Public 1311oday</td>
      <td>0.294118</td>
      <td>0.294118</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>520521</td>
      <td>Sen. MARY GEORGE (R)<br><br>Senate Minority Leader</td>
      <td>sen. MARY GEORGE (R)<br><br>Senate Minority Leader</td>
      <td>0.022727</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>546380</td>
      <td>Rep. PETER APO (D)<br><br>House Majority Floor Leader</td>
      <td>Rep. PETER APO U<br><br>House Majority-Floor Leader</td>
      <td>0.088889</td>
      <td>0.088889</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>647014</td>
      <td>Rep. ROLAND KOTANI (D)<br><br>Pearl City/Pacific Palisades</td>
      <td>Rep. INVTOU KOTANT (D)<br><br>Pearl Gity/Pacitic Palisades</td>
      <td>0.173077</td>
      <td>0.173077</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>677010</td>
      <td>Sen. ELOISE TUNGPALAN (D)<br><br>Chairman, Senate Culture<br><br>& Arts Committee</td>
      <td>Sen. ELOISE ANTVONNIA D<br><br>Chairman, Senate. Culture<br><br>2 Arts Committee</td>
      <td>0.191176</td>
      <td>0.191176</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>778779</td>
      <td>Sen. RICK REED (R)<br><br>Senate Minority Floor Leader</td>
      <td>Sen. RICK REED (R)<br><br>Senate Minority Floor Leader</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>800400</td>
      <td>Sen. GERALD HAGINO (D)<br><br>Senate Majority Leader</td>
      <td>Sen. GERALD HAGINO (D)<br><br>Senate Majority Leader</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>849516</td>
      <td>Sen. RUSSELL BLAIR (D)<br><br>Senate Majority Floor Leader</td>
      <td>Sen. TTESSN BLAIR D<br><br>Senate Majority Floor Leader</td>
      <td>0.163265</td>
      <td>0.163265</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (27 rows)</td>
      <td>948782</td>
      <td>Rep. DWIGHT TAKAMINE (D)<br><br>North Hilo/Hamakua</td>
      <td>Rep. DWIGHT TAKAMINE (D<br><br>North Hilo/Hamakua</td>
      <td>0.023256</td>
      <td>0.023256</td>
    </tr>
  </tbody>
</table>