## Data specs
- Groundtruth data location: KeyedInformationExtraction/golds_test'
- System prediction (MMIF) location: KeyedInformationExtraction/llava_preds'

## Pipeline specs

## Raw Results
```
GUID,mean-CER-cased,mean-CER-uncased
cpb-aacip-225-12z34w2c,"[0.5714285714285714, 0.826863136863137, 0.9714285714285714]","[0.5714285714285714, 0.39174825174825173, 0.8714285714285713]" 
cpb-aacip-225-15bcc3x8,"[1.0, 0.4242424242424242, 0.9285714285714286]","[1.0, 0.3787878787878788, 0.9285714285714286]"
cpb-aacip-225-20ftth6f,"[0.9375, 0.7186189200830244, 0.9336754680504681]","[0.9375, 0.39289448156242524, 0.9313606532356532]"
cpb-aacip-225-27zkh3tm,"[1.0, 0.9085568538106268, 1.0]","[1.0, 0.7741763881623128, 1.0]"
cpb-aacip-225-31qftxh5,"[1.0, 0.6347972972972973, 1.0]","[1.0, 0.5972972972972973, 1.0]"
cpb-aacip-225-37vmd093,"[1.713690517466261, 1.1153741817390832, 0.9517895056020859]","[1.713690517466261, 0.8994002929450069, 0.9362924101049902]"   
cpb-aacip-225-44bnzxh7,"[0.8181818181818182, 0.6439452588388759, 0.9542398777692895]","[0.8181818181818182, 0.3212177499411542, 0.9403106697224345]" 
cpb-aacip-225-48sbchm7,"[0.8, 0.5167105263157895, 0.8543024227234752]","[0.8, 0.14407894736842106, 0.8363686995265942]"
cpb-aacip-225-51vdnj5t,"[1.0, 0.2946997929606625, 0.8181395348837208]","[1.0, 0.285175983436853, 0.7108062015503875]"
cpb-aacip-225-65v6x41w,"[0.5, 0.775, 0.9473684210526316]","[0.5, 0.19642857142857142, 0.9473684210526316]"

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
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>188155</td>
      <td>{'name-as-written': 'GEORGE TAKANE', 'name-normalized': 'Takane, George', 'attributes': ['HOUSE CLERK']}</td>
      <td>{'name-as-written': 'George Takane House Clerk', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.88, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.48, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>525759</td>
      <td>{'name-as-written': 'JAY LARRIN', 'name-normalized': 'Larrin, Jay', 'attributes': []}</td>
      <td>{'name-as-written': 'Jay Larrin', 'name-normalized': 'LARRIN JAY', 'attributes': []}</td>
      <td>{'name-as-written': 0.7, 'name-normalized': 0.8, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.1, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>686019</td>
      <td>{'name-as-written': 'LOYAL GARNER', 'name-normalized': 'Garner, Loyal', 'attributes': []}</td>
      <td>{'name-as-written': 'Loyal Garner', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.75, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>701268</td>
      <td>{'name-as-written': 'RICHARD S. H. WONG', 'name-normalized': 'Wong, Richard S. H.', 'attributes': ['SENATE PRESIDENT']}</td>
      <td>{'name-as-written': 'Richard s h wong senate president', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8787878787878788, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5757575757575758, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>790390</td>
      <td>{'name-as-written': 'REV. WILLIAM KAINA', 'name-normalized': 'Kaina, William', 'attributes': []}</td>
      <td>{'name-as-written': 'William Kaina Rev., William Kaina', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8181818181818182, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.45454545454545453, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>1000400</td>
      <td>{'name-as-written': 'DAVID WOO', 'name-normalized': 'Woo, David', 'attributes': ['SENATE CLERK']}</td>
      <td>{'name-as-written': 'David Woo Senate Clerk', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8636363636363636, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5909090909090909, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>1176009</td>
      <td>{'name-as-written': 'STACY SAKAMOTO', 'name-normalized': 'Sakamoto, Stacy', 'attributes': ['HAWAII PUBLIC TELEVISION']}</td>
      <td>{'name-as-written': 'Stacy Sakamoto Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8974358974358975, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6410256410256411, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>245145</td>
      <td>{'name-as-written': 'Ted Liu', 'name-normalized': 'Liu, Ted', 'attributes': ['Director', 'DBEDT']}</td>
      <td>{'name-as-written': 'Ted Liu Director DBEI', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6666666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6666666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>640507</td>
      <td>{'name-as-written': 'Mark Sasaki', 'name-normalized': 'Sasaki, Mark', 'attributes': ['Big City Diner']}</td>
      <td>{'name-as-written': 'Mark sakaki', 'name-normalized': 'Big city diner', 'attributes': []}</td>
      <td>{'name-as-written': 0.18181818181818182, 'name-normalized': 0.8571428571428571, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.09090909090909091, 'name-normalized': 0.8571428571428571, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>105506</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Edition']}</td>
      <td>{'name-as-written': 'Lynnette Lo Tom Hawaii Edition', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8333333333333334, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5333333333333333, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>202135</td>
      <td>{'name-as-written': 'PHIL ESTERMAN', 'name-normalized': 'Esterman, Phil', 'attributes': ['Save Sandy Beach Coalition']}</td>
      <td>{'name-as-written': 'Phil Estermann', 'name-normalized': 'Save Sandy Beach Coalition', 'attributes': []}</td>
      <td>{'name-as-written': 0.7857142857142857, 'name-normalized': 0.7692307692307693, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.07142857142857142, 'name-normalized': 0.7692307692307693, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>230764</td>
      <td>{'name-as-written': 'STEVE HIRANO', 'name-normalized': 'Hirano, Steve', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'STEVE HIRANO', 'name-normalized': 'Good Neighbors / Good Planning', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8666666666666667, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8666666666666667, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>248282</td>
      <td>{'name-as-written': 'DONNA GOTH', 'name-normalized': 'Goth, Donna', 'attributes': ['Land Use Research Foundation of Hawaii']}</td>
      <td>{'name-as-written': 'Donna Goth Land Use Research Foundation of Hawaii', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9183673469387755, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7959183673469388, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>301001</td>
      <td>{'name-as-written': 'KELLY DEAN', 'name-normalized': 'Dean, Kelly', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'KELLY DEAN HAWAII PUBLIC TELEVISION', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7142857142857143, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7142857142857143, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>321522</td>
      <td>{'name-as-written': 'JOANN YUKIMURA (D)', 'name-normalized': 'Yukimura, Joann', 'attributes': ['Kauai Mayor']}</td>
      <td>{'name-as-written': 'Joann Yukimura D) Kauai Mayor', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8275862068965517, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.4482758620689655, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>360027</td>
      <td>{'name-as-written': 'REP. EZRA KANOHO (D)', 'name-normalized': 'Kanoho, Ezra', 'attributes': ['Lihue/Kapaa']}</td>
      <td>{'name-as-written': 'Representative Ezra Kanoho D( Lihue / Kapaaa )', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8260869565217391, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6086956521739131, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>437504</td>
      <td>{'name-as-written': 'GOV. JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': []}</td>
      <td>{'name-as-written': 'GOV., JOHN WAIHEE(D)', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.1, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.1, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>494528</td>
      <td>{'name-as-written': 'GARY GILL', 'name-normalized': 'Gill, Gary', 'attributes': ['Honolulu City Council Member']}</td>
      <td>{'name-as-written': 'GARY GILL HONOLULU CITY COUNCIL MEMBER', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7631578947368421, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7631578947368421, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>532900</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'John Radcliffe', 'name-normalized': 'Good Neighbors / Good Planning', 'attributes': []}</td>
      <td>{'name-as-written': 0.7857142857142857, 'name-normalized': 0.8333333333333334, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8333333333333334, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>598632</td>
      <td>{'name-as-written': 'GARY GILL', 'name-normalized': 'Gill, Gary', 'attributes': ['Honolulu City Council Member']}</td>
      <td>{'name-as-written': 'GARY GILL HONOLULU CITY COUNCIL MEMBER', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7631578947368421, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7631578947368421, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>640774</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'John Radcliffe', 'name-normalized': 'Good Neighbors Good Planning', 'attributes': []}</td>
      <td>{'name-as-written': 0.7857142857142857, 'name-normalized': 0.8214285714285714, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8214285714285714, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>884751</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'John Radgiffe', 'name-normalized': 'Good Neighbors / Good Planning', 'attributes': []}</td>
      <td>{'name-as-written': 0.8461538461538461, 'name-normalized': 0.8333333333333334, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.15384615384615385, 'name-normalized': 0.8333333333333334, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1021755</td>
      <td>{'name-as-written': 'MARTHA HULBERT', 'name-normalized': 'Hulbert, Martha', 'attributes': ['Adoption Circle of Hawaii']}</td>
      <td>{'name-as-written': 'Marttha Hulbert Adoption Circle Of Hawaii', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9024390243902439, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6585365853658537, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1183016</td>
      <td>{'name-as-written': 'VERA BENEDEK', 'name-normalized': 'Benedek, Vera', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'Vera Benedek Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.918918918918919, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6756756756756757, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1308141</td>
      <td>{'name-as-written': 'ARTHUR ROSS', 'name-normalized': 'Ross, Arthur', 'attributes': ['Neighborhood Board Chairman']}</td>
      <td>{'name-as-written': 'Arthur Ross', 'name-normalized': 'Neighborhood Board Chairman', 'attributes': []}</td>
      <td>{'name-as-written': 0.7272727272727273, 'name-normalized': 0.8148148148148148, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.7777777777777778, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>96763</td>
      <td>{'name-as-written': 'DAN BOYLAN', 'name-normalized': 'Boylan, Dan', 'attributes': ['Newsmakers']}</td>
      <td>{'name-as-written': 'Dan Boylan Newsmakers', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8095238095238095, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5238095238095238, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>149016</td>
      <td>{'name-as-written': 'WHITNEY ANDERSON (R)', 'name-normalized': 'Anderson, Whitney', 'attributes': ['State Senate Candidate', 'District 25 Kailua, Waimanalo']}</td>
      <td>{'name-as-written': 'Whitney Anderson(R) State Senate Candidate District 25 Kahalu Waianaeo Whitney Anderson is speaking about his campaign for state senate candidate from district 25 kahulu waiananea oahu hawaii', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9685863874345549, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.9057591623036649, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>312779</td>
      <td>{'name-as-written': 'FRED HEMMINGS (R)', 'name-normalized': 'Hemmings, Fred', 'attributes': ['State Senate Candidate', 'District 25 Kailua, Waimanalo']}</td>
      <td>{'name-as-written': 'Fred Heggings(R) State Senate Candidate District 25 Kailua, Waimanalo', 'name-normalized': '', 'attributes': []}</td> 
      <td>{'name-as-written': 0.927536231884058, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.8115942028985508, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>933767</td>
      <td>{'name-as-written': 'ALEX SONSON (D)', 'name-normalized': 'Sonson, Alex', 'attributes': ['State Rep. Candidate', 'District 36 Pearl City, Waipahu']}</td>
      <td>{'name-as-written': 'Alex Sonson(dj) State Rep., Candidate District 36 Pearl City Waipahu', 'name-normalized': '', 'attributes': []}</td>  
      <td>{'name-as-written': 0.9117647058823529, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.8088235294117647, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>985652</td>
      <td>{'name-as-written': 'ROY TAKUMI (D)', 'name-normalized': 'Takumi, Roy', 'attributes': ['State Rep. Candidate', 'District 36 Pearl City, Waipahu']}</td>
      <td>{'name-as-written': 'Roy Takumi(d) State Rep., Candidate District 36 Pearl City, Waimahu', 'name-normalized': '', 'attributes': []}</td>   
      <td>{'name-as-written': 0.9253731343283582, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.8208955223880597, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-31qftxh5 (6 rows)</td>
      <td>824391</td>
      <td>{'name-as-written': 'Joseph M. Souki (D)', 'name-normalized': 'Souki, Joseph M.', 'attributes': ['Speaker of the House']}</td>
      <td>{'name-as-written': 'Joseph m s souki(d) speaker of the house', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.675, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-31qftxh5 (6 rows)</td>
      <td>993126</td>
      <td>{'name-as-written': 'Tom Okamura (D)', 'name-normalized': 'Okamura, Tom', 'attributes': ['House Majority Leader']}</td>
      <td>{'name-as-written': 'Tom Okamura (D) House Majority Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5945945945945946, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5945945945945946, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>88889</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'Lynnette Lo Tom Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.875, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.65, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>119253</td>
      <td>{'name-as-written': 'JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': ['Governor']}</td>
      <td>{'name-as-written': 'John Waihee D) Governor', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.782608695652174, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.43478260869565216, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>174775</td>
      <td>{'name-as-written': 'Rep. SAMUEL LEE (D)', 'name-normalized': 'Lee, Samuel', 'attributes': ['Vice Chairman', 'House Education Committee']}</td>
      <td>{'name-as-written': 'Representative Samuel Lee D( Vice Chairman House Education Committee)', 'name-normalized': '', 'attributes': []}</td> 
      <td>{'name-as-written': 0.855072463768116, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7391304347826086, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>185886</td>
      <td>{'name-as-written': 'Sen. BERTRAND KOBAYASHI (D)', 'name-normalized': 'Kobayashi, Bertrand', 'attributes': ['Chairman, Senate Education Committee']}</td>
      <td>{'name-as-written': '```markdown', 'name-normalized': 'SEN., BERTRANDB KOBAYASHI D(Chairman, Senate Education Committee)', 'attributes': ['Kobayashi, Bertrand', '```']}</td>
      <td>{'name-as-written': 2.4545454545454546, 'name-normalized': 0.8615384615384616, 'attributes': 1.3636363636363635}</td>
      <td>{'name-as-written': 2.1818181818181817, 'name-normalized': 0.7692307692307693, 'attributes': 1.3636363636363635}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>214281</td>
      <td>{'name-as-written': 'Rep. ROD TAM (D)', 'name-normalized': 'Tam, Rod', 'attributes': ['Chairman', 'House Education Committee']}</td>       
      <td>{'name-as-written': 'Representative Rod Tam D( Chairman House Education Committee )', 'name-normalized': '', 'attributes': []}</td>        
      <td>{'name-as-written': 0.8387096774193549, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7580645161290323, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>255255</td>
      <td>{'name-as-written': 'Rep. BOB McEACHERN', 'name-normalized': 'McEachern, Bob', 'attributes': ['Minnesota Legislator']}</td>
      <td>{'name-as-written': 'Representative Bob McEachern Minnesota Legislature', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.82, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.66, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>295529</td>
      <td>{'name-as-written': 'Sen. MIKE McCARTNEY (D)', 'name-normalized': 'McCartney, Mike', 'attributes': ['Vice Chairman', 'Senate Education Committee']}</td>
      <td>{'name-as-written': 'Name: Mike McCartney D)', 'name-normalized': 'Normalized Name: Mc Cartney Michael David', 'attributes': ['Role: Vice Chairman Senate Education Committee']}</td>
      <td>{'name-as-written': 0.6521739130434783, 'name-normalized': 0.7073170731707317, 'attributes': 0.15217391304347827}</td>
      <td>{'name-as-written': 0.2608695652173913, 'name-normalized': 0.7073170731707317, 'attributes': 0.15217391304347827}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>414281</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'Lynnette Lo Tom Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.875, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.65, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>447648</td>
      <td>{'name-as-written': 'EVAN THOMAS', 'name-normalized': 'Thomas, Evan', 'attributes': ['Common Cause']}</td>
      <td>{'name-as-written': 'Evan Thomas Common Cause', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.875, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5416666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>461128</td>
      <td>{'name-as-written': 'PATSY T. MINK', 'name-normalized': 'Mink, Patsy T.', 'attributes': ['The Public Reporter']}</td>
      <td>{'name-as-written': 'Patsy Tink The Public Reporter', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8333333333333334, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>520521</td>
      <td>{'name-as-written': 'Sen. MARY GEORGE (R)', 'name-normalized': 'George, Mary', 'attributes': ['Senate Minority Leader']}</td>
      <td>{'name-as-written': '```markdown', 'name-normalized': 'SEN., MARY GEORGE (R) Senate Minority Leader', 'attributes': ['George, Mary Senator from Minnesota', '```']}</td>
      <td>{'name-as-written': 1.8181818181818181, 'name-normalized': 0.8636363636363636, 'attributes': 0.7368421052631579}</td>
      <td>{'name-as-written': 1.4545454545454546, 'name-normalized': 0.7727272727272727, 'attributes': 0.7368421052631579}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>546380</td>
      <td>{'name-as-written': 'Rep. PETER APO (D)', 'name-normalized': 'Apo, Peter', 'attributes': ['House Majority Floor Leader']}</td>
      <td>{'name-as-written': 'Representative Peter Apo(d) House Majority Floor Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8545454545454545, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7272727272727273, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>607007</td>
      <td>{'name-as-written': 'JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': ['Governor']}</td>
      <td>{'name-as-written': 'John Waihee D) Governor', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.782608695652174, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.43478260869565216, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>647014</td>
      <td>{'name-as-written': 'Rep. ROLAND KOTANI (D)', 'name-normalized': 'Kotani, Roland', 'attributes': ['Pearl City/Pacific Palisades']}</td>    
      <td>{'name-as-written': 'Representative Roland Kotani(d) Pearl City / Pacific Palisades', 'name-normalized': '', 'attributes': []}</td>        
      <td>{'name-as-written': 0.8709677419354839, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6935483870967742, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>677010</td>
      <td>{'name-as-written': 'Sen. ELOISE TUNGPALAN (D)', 'name-normalized': 'Tungpalan, Eloise', 'attributes': ['Chairman, Senate Culture & Arts Committee']}</td>
      <td>{'name-as-written': '```markdown', 'name-normalized': 'SEN., ELOISE TUNGPalan D)', 'attributes': ['Chairman, Senate Culture & Arts Committee', '```']}</td>
      <td>{'name-as-written': 2.272727272727273, 'name-normalized': 0.92, 'attributes': 0.06818181818181818}</td>
      <td>{'name-as-written': 2.1818181818181817, 'name-normalized': 0.8, 'attributes': 0.06818181818181818}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>778779</td>
      <td>{'name-as-written': 'Sen. RICK REED (R)', 'name-normalized': 'Reed, Rick', 'attributes': ['Senate Minority Floor Leader']}</td>
      <td>{'name-as-written': '```markdown', 'name-normalized': 'Rick Reed (R) Senate Minority Floor Leader Sen., Rick Reed R(eckerd@aol.com)', 'attributes': ['```']}</td>
      <td>{'name-as-written': 1.6363636363636365, 'name-normalized': 0.868421052631579, 'attributes': 9.333333333333334}</td>
      <td>{'name-as-written': 1.3636363636363635, 'name-normalized': 0.868421052631579, 'attributes': 9.333333333333334}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>800400</td>
      <td>{'name-as-written': 'Sen. GERALD HAGINO (D)', 'name-normalized': 'Hagino, Gerald', 'attributes': ['Senate Majority Leader']}</td>
      <td>{'name-as-written': 'Gerald Hagino D) Senate Majority Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8717948717948718, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7435897435897436, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>849516</td>
      <td>{'name-as-written': 'Sen. RUSSELL BLAIR (D)', 'name-normalized': 'Blair, Russell', 'attributes': ['Senate Majority Floor Leader']}</td>    
      <td>{'name-as-written': '```markdown', 'name-normalized': 'Russell Blair D) Senate Majority Floor Leader', 'attributes': ['```']}</td>
      <td>{'name-as-written': 2.0, 'name-normalized': 0.8222222222222222, 'attributes': 9.333333333333334}</td>
      <td>{'name-as-written': 1.9090909090909092, 'name-normalized': 0.8, 'attributes': 9.333333333333334}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>948782</td>
      <td>{'name-as-written': 'Rep. DWIGHT TAKAMINE (D)', 'name-normalized': 'Takamine, Dwight', 'attributes': ['North Hilo/Hamakua']}</td>
      <td>{'name-as-written': 'Representative Dwight Takamine(R)', 'name-normalized': 'North Hilo Hamakua', 'attributes': []}</td>
      <td>{'name-as-written': 0.7575757575757576, 'name-normalized': 0.9444444444444444, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.3939393939393939, 'name-normalized': 0.9444444444444444, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>1080013</td>
      <td>{'name-as-written': 'Rep. DAVID IGE (D)', 'name-normalized': 'Ige, David', 'attributes': ['Chairman, Economic Dev. & Hawaiian Affairs Com.']}</td>
      <td>{'name-as-written': 'Representative David Ige D( Chairman, Economic Deve & Hawaiian Affairs Com.,)', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8571428571428571, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7792207792207793, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>1295028</td>
      <td>{'name-as-written': 'Sen. LEHUA FERNANDES SALLING (D)', 'name-normalized': 'Fernandes Salling, Lehua', 'attributes': ['Chairman', 'Senate Transportation Committee']}</td>
      <td>{'name-as-written': 'Name: Sen., Lehua Fernandes Salting D( Chairman Senate Transportation Committee )', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8395061728395061, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6296296296296297, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>108275</td>
      <td>{'name-as-written': 'LESLIE WILCOX', 'name-normalized': 'Wilcox, Leslie', 'attributes': ['ELECTION LIVE']}</td>
      <td>{'name-as-written': 'Leslie Wilcox Election Live', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8518518518518519, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5185185185185185, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>270904</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Former Congressional Candidate']}</td>
      <td>{'name-as-written': 'John Radcliffe Former Congressional Candidate', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9111111111111111, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>347514</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Keir, Gerry', 'attributes': ['Managing Editor', 'Honolulu Advertiser']}</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Managing Editor Honolulu Advertiser', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8571428571428571, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8285714285714286, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>422756</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Former Congressional Candidate']}</td>
      <td>{'name-as-written': 'John Radcliffe', 'name-normalized': 'Former Congressional Candidate', 'attributes': []}</td>
      <td>{'name-as-written': 0.7857142857142857, 'name-normalized': 0.9, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8333333333333334, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>488522</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Keir, Gerry', 'attributes': ['Managing Editor', 'Honolulu Advertiser']}</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Managing Editor Honolulu Advertiser', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8571428571428571, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8285714285714286, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>784151</td>
      <td>{'name-as-written': 'NINA BERGLUND', 'name-normalized': 'Berglund, Nina', 'attributes': ['Election Live']}</td>
      <td>{'name-as-written': '215 Campaign Spending Commission Office Of The Lieutenant Governor Nina Berglund Election Live', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9468085106382979, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.8617021276595744, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>801635</td>
      <td>{'name-as-written': 'DAN TUTTLE', 'name-normalized': 'Tuttle, Dan', 'attributes': ['Political Analyst']}</td>
      <td>{'name-as-written': 'Dan Tuttle Political Analyst', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8928571428571429, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6428571428571429, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>830030</td>
      <td>{'name-as-written': 'ANDREW POEPOE', 'name-normalized': 'Poepoe, Andrew', 'attributes': ['Co-Chairman', 'Saiki in '88 Committee']}</td>    
      <td>{'name-as-written': 'Andrew Poepoe', 'name-normalized': 'Co-Chairman Saiki in '88 Committee', 'attributes': []}</td>
      <td>{'name-as-written': 0.7692307692307693, 'name-normalized': 0.8823529411764706, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8529411764705882, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1068902</td>
      <td>{'name-as-written': 'STAN KOKI (R)', 'name-normalized': 'Koki, Stan', 'attributes': []}</td>
      <td>{'name-as-written': 'Stan Koki (R)', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.46153846153846156, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1183016</td>
      <td>{'name-as-written': 'CLAYTON HEE (D)', 'name-normalized': 'Hee, Clayton', 'attributes': []}</td>
      <td>{'name-as-written': 'Clayton Hee(d)', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7142857142857143, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.07142857142857142, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1417150</td>
      <td>{'name-as-written': 'JERRY BURRIS', 'name-normalized': 'Burris, Jerry', 'attributes': ['Politics Editor', 'Honolulu Advertiser']}</td>     
      <td>{'name-as-written': 'JERRY BURRIS POLITICS EDITOR HONOLULU ADVERTiser', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.75, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.75, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>97397</td>
      <td>{'name-as-written': 'LESLIE WILCOX', 'name-normalized': 'Wilcox, Leslie', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'Leslie Wilcox Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9210526315789473, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6578947368421053, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>175876</td>
      <td>{'name-as-written': 'JONATHAN DENNIS', 'name-normalized': 'Dennis, Jonathan', 'attributes': ['Director, The New Zealand Film Archive']}</td>
      <td>{'name-as-written': 'Jonathan Dennis', 'name-normalized': 'Director, The New Zealand Film Archive', 'attributes': []}</td>
      <td>{'name-as-written': 0.8, 'name-normalized': 0.8421052631578947, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8157894736842105, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>581381</td>
      <td>{'name-as-written': 'WITARINA HARRIS', 'name-normalized': 'Harris, Witarina', 'attributes': []}</td>
      <td>{'name-as-written': 'WITA RINA HARRIS', 'name-normalized': 'Hostess for game show', 'attributes': []}</td>
      <td>{'name-as-written': 0.0625, 'name-normalized': 0.8095238095238095, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0625, 'name-normalized': 0.8095238095238095, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>955255</td>
      <td>{'name-as-written': 'WITARINA HARRIS', 'name-normalized': 'Harris, Witarina', 'attributes': []}</td>
      <td>{'name-as-written': 'WITARINA HARRIS', 'name-normalized': 'Older woman wearing glasses', 'attributes': ['Pink shirt']}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.7777777777777778, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.7407407407407407, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>1404404</td>
      <td>{'name-as-written': 'JONATHAN DENNIS', 'name-normalized': 'Dennis, Jonathan', 'attributes': ['Director, The New Zealand Film Archive']}</td>
      <td>{'name-as-written': 'Jonathan Dennis', 'name-normalized': 'Director, The New Zealand Film Archive', 'attributes': []}</td>
      <td>{'name-as-written': 0.8, 'name-normalized': 0.8421052631578947, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8157894736842105, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>99766</td>
      <td>{'name-as-written': 'Howard Dicus', 'name-normalized': 'Dicus, Howard', 'attributes': ['PBN Friday']}</td>
      <td>{'name-as-written': 'Howard Dicus PBN Friday', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.4782608695652174, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.4782608695652174, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>286753</td>
      <td>{'name-as-written': 'Connie Lau', 'name-normalized': 'Lau, Connie', 'attributes': ['CEO', 'American Savings Bank']}</td>
      <td>{'name-as-written': 'Connie Lau', 'name-normalized': 'CEO American Savings Bank', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.92, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.84, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>644878</td>
      <td>{'name-as-written': 'Sterling Paulos', 'name-normalized': 'Paulos, Sterling', 'attributes': ['Hotel Director', 'NCL Hawaii']}</td>
      <td>{'name-as-written': 'Stirling Paulos', 'name-normalized': 'Hotel Director NCL Hawaii', 'attributes': []}</td>
      <td>{'name-as-written': 0.06666666666666667, 'name-normalized': 0.88, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.06666666666666667, 'name-normalized': 0.84, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>954521</td>
      <td>{'name-as-written': 'Susan Todani', 'name-normalized': 'Todani, Susan', 'attributes': ['Director of Investments', 'Kamehameha Schools']}</td>
      <td>{'name-as-written': 'Director of Investments KAMEHANEHA Schools', 'name-normalized': 'TODANI Susan', 'attributes': []}</td>
      <td>{'name-as-written': 0.9285714285714286, 'name-normalized': 0.5, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.8809523809523809, 'name-normalized': 0.08333333333333333, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>1032032</td>
      <td>{'name-as-written': 'Rosalind Schurgin', 'name-normalized': 'Schurgin, Rosalind', 'attributes': ['Executive Vice President', 'Festival Companies']}</td>
      <td>{'name-as-written': 'Rosalind Schurgin', 'name-normalized': 'Executive Vice President Festival Companies', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.7906976744186046, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.7906976744186046, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-65v6x41w (18 rows)</td>
      <td>250150</td>
      <td>{'name-as-written': 'CHARLES TOGUCHI', 'name-normalized': 'Toguchi, Charles', 'attributes': ['Superintendent', 'Dept. of Education']}</td> 
      <td>{'name-as-written': 'Charles Toguchi', 'name-normalized': 'Superintendent Department Of Education', 'attributes': []}</td>
      <td>{'name-as-written': 0.8, 'name-normalized': 0.8947368421052632, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.8947368421052632, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-65v6x41w (18 rows)</td>
      <td>1179646</td>
      <td>{'name-as-written': 'Rep. DANIEL KIHANO', 'name-normalized': 'Kihano, Daniel', 'attributes': []}</td>
      <td>{'name-as-written': 'Representative Daniel Kihano', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.75, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.39285714285714285, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
  </tbody>
</table>

## Data specs
- Groundtruth data location: KeyedInformationExtraction/golds_test'
- System prediction (MMIF) location: KeyedInformationExtraction/tesseract_preds'

## Pipeline specs

## Raw Results
```
GUID,mean-CER-cased,mean-CER-uncased
cpb-aacip-225-12z34w2c,"[0.5769230769230769, 6.5, 7.0]","[0.5769230769230769, 6.5, 7.0]"
cpb-aacip-225-15bcc3x8,"[1.384057971014493, 9.0, 10.0]","[1.384057971014493, 9.0, 10.0]"
cpb-aacip-225-20ftth6f,"[1.0540965207631874, 2.3666666666666667, 1.8484848484848484]","[1.0294051627384961, 2.3666666666666667, 1.707070707070707]"  
cpb-aacip-225-27zkh3tm,"[1.0, 10.0, 11.0]","[1.0, 10.0, 11.0]"
cpb-aacip-225-31qftxh5,-1,-1
cpb-aacip-225-37vmd093,"[0.39769230769230773, 7.111111111111111, 6.368421052631579]","[0.39769230769230773, 7.111111111111111, 5.842105263157895]"   
cpb-aacip-225-44bnzxh7,"[1.0, 7.653846153846154, 6.1875]","[1.0, 7.653846153846154, 6.125]"
cpb-aacip-225-48sbchm7,False,False
cpb-aacip-225-51vdnj5t,"[0.8494824016563146, 2.7777777777777772, 2.5256410256410255]","[0.4608695652173913, 2.194444444444444, 2.358974358974359]"   
cpb-aacip-225-65v6x41w,-1,-1

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
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>188155</td>
      <td>{'name-as-written': 'GEORGE TAKANE', 'name-normalized': 'Takane, George', 'attributes': ['HOUSE CLERK']}</td>
      <td>{'name-as-written': '@\', 'name-normalized': '@\', 'attributes': ['GEORGE TAKANE', 'HOUSE CLERK =']}</td>
      <td>{'name-as-written': 6.5, 'name-normalized': 7.0, 'attributes': 0.5769230769230769}</td>
      <td>{'name-as-written': 6.5, 'name-normalized': 7.0, 'attributes': 0.5769230769230769}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>245145</td>
      <td>{'name-as-written': 'Ted Liu', 'name-normalized': 'Liu, Ted', 'attributes': ['Director', 'DBEDT']}</td>
      <td>{'name-as-written': 'Y', 'name-normalized': 'Y', 'attributes': ['ae', 'Te Liv X', 'Director', 'DBEDT']}</td>
      <td>{'name-as-written': 7.0, 'name-normalized': 8.0, 'attributes': 0.43478260869565216}</td>
      <td>{'name-as-written': 7.0, 'name-normalized': 8.0, 'attributes': 0.43478260869565216}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>640507</td>
      <td>{'name-as-written': 'Mark Sasaki', 'name-normalized': 'Sasaki, Mark', 'attributes': ['Big City Diner']}</td>
      <td>{'name-as-written': '=', 'name-normalized': '=', 'attributes': ['a', '=', 'a', '=', '=', '=']}</td>
      <td>{'name-as-written': 11.0, 'name-normalized': 12.0, 'attributes': 2.3333333333333335}</td>
      <td>{'name-as-written': 11.0, 'name-normalized': 12.0, 'attributes': 2.3333333333333335}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>301001</td>
      <td>{'name-as-written': 'KELLY DEAN', 'name-normalized': 'Dean, Kelly', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'NE;', 'name-normalized': 'Ne;', 'attributes': ['nade oe ion']}</td>
      <td>{'name-as-written': 3.0, 'name-normalized': 3.3333333333333335, 'attributes': 1.6363636363636365}</td>
      <td>{'name-as-written': 3.0, 'name-normalized': 3.0, 'attributes': 1.6363636363636365}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>360027</td>
      <td>{'name-as-written': 'REP. EZRA KANOHO (D)', 'name-normalized': 'Kanoho, Ezra', 'attributes': ['Lihue/Kapaa']}</td>
      <td>{'name-as-written': '< : 4', 'name-normalized': ': 4, <', 'attributes': ['Am', '* ¥', 'REP. EZRA KAMoHO (BD)', 'a']}</td>
      <td>{'name-as-written': 3.6, 'name-normalized': 1.6666666666666667, 'attributes': 0.9259259259259259}</td>
      <td>{'name-as-written': 3.6, 'name-normalized': 1.6666666666666667, 'attributes': 0.8518518518518519}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1183016</td>
      <td>{'name-as-written': 'VERA BENEDEK', 'name-normalized': 'Benedek, Vera', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'VERA’ B NE', 'name-normalized': 'B Ne, Vera’', 'attributes': ['as Public el ev revi']}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 0.5454545454545454, 'attributes': 0.6}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 0.45454545454545453, 'attributes': 0.6}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>96763</td>
      <td>{'name-as-written': 'DAN BOYLAN', 'name-normalized': 'Boylan, Dan', 'attributes': ['Newsmakers']}</td>
      <td>{'name-as-written': 'J', 'name-normalized': 'J', 'attributes': []}</td>
      <td>{'name-as-written': 10.0, 'name-normalized': 11.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 10.0, 'name-normalized': 11.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>119253</td>
      <td>{'name-as-written': 'JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': ['Governor']}</td>
      <td>{'name-as-written': 'N', 'name-normalized': 'N', 'attributes': ['JOHN WAIHEE (D)', 'Governor', '1%']}</td>
      <td>{'name-as-written': 14.0, 'name-normalized': 12.0, 'attributes': 0.68}</td>
      <td>{'name-as-written': 14.0, 'name-normalized': 11.0, 'attributes': 0.68}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>414281</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': '%* gLYNETTE LO TOM', 'name-normalized': 'Glynette Lo Tom, %*', 'attributes': ['~iawaii Public Television', '~']}</td> 
      <td>{'name-as-written': 0.2222222222222222, 'name-normalized': 0.7368421052631579, 'attributes': 0.11538461538461539}</td>
      <td>{'name-as-written': 0.2222222222222222, 'name-normalized': 0.6842105263157895, 'attributes': 0.11538461538461539}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1068902</td>
      <td>{'name-as-written': 'STAN KOKI (R)', 'name-normalized': 'Koki, Stan', 'attributes': []}</td>
      <td>{'name-as-written': 'STA OKI (R) =', 'name-normalized': 'Oki, Sta', 'attributes': ['ie']}</td>
      <td>{'name-as-written': 0.3076923076923077, 'name-normalized': 0.375, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.3076923076923077, 'name-normalized': 0.25, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1183016</td>
      <td>{'name-as-written': 'CLAYTON HEE (D)', 'name-normalized': 'Hee, Clayton', 'attributes': []}</td>
      <td>{'name-as-written': '«', 'name-normalized': '«', 'attributes': ['/ CLAYTON HEE (D)', 'ow” — a 4']}</td>
      <td>{'name-as-written': 15.0, 'name-normalized': 12.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 15.0, 'name-normalized': 12.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>99766</td>
      <td>{'name-as-written': 'Howard Dicus', 'name-normalized': 'Dicus, Howard', 'attributes': ['PBN Friday']}</td>
      <td>{'name-as-written': 'Howaro Dicus', 'name-normalized': 'Dicus, Howaro', 'attributes': ['PBN FRIDAY']}</td>
      <td>{'name-as-written': 0.08333333333333333, 'name-normalized': 0.07692307692307693, 'attributes': 0.5}</td>
      <td>{'name-as-written': 0.08333333333333333, 'name-normalized': 0.07692307692307693, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>644878</td>
      <td>{'name-as-written': 'Sterling Paulos', 'name-normalized': 'Paulos, Sterling', 'attributes': ['Hotel Director', 'NCL Hawaii']}</td>
      <td>{'name-as-written': 'AS', 'name-normalized': 'As', 'attributes': ['STERLING PAULOS', 'Hove DiRecroR', 'NCL Haw']}</td>
      <td>{'name-as-written': 7.5, 'name-normalized': 7.5, 'attributes': 0.6571428571428571}</td>
      <td>{'name-as-written': 6.5, 'name-normalized': 7.0, 'attributes': 0.6}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>954521</td>
      <td>{'name-as-written': 'Susan Todani', 'name-normalized': 'Todani, Susan', 'attributes': ['Director of Investments', 'Kamehameha Schools']}</td>
      <td>{'name-as-written': 'SUSAN TODANI', 'name-normalized': 'Todani, Susan', 'attributes': ['DIRECTOR OF InvesTMENTS']}</td>
      <td>{'name-as-written': 0.75, 'name-normalized': 0.0, 'attributes': 1.391304347826087}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.782608695652174}</td>
    </tr>
  </tbody>
</table>

## Data specs
- Groundtruth data location: ./KeyedInformationExtraction/golds_test'
- System prediction (MMIF) location: ./KeyedInformationExtraction/doctr_preds'

## Pipeline specs

## Raw Results
```
GUID,mean-CER-cased,mean-CER-uncased
cpb-aacip-225-12z34w2c,False,False
cpb-aacip-225-15bcc3x8,"[0.679945054945055, 0.7330827067669172, 0.425]","[0.25, 0.39473684210526316, 0.4]"
cpb-aacip-225-20ftth6f,"[0.6149422912928819, 3.1906822344322343, 3.033452831890332]","[0.5856708048641375, 3.181753663003663, 3.033452831890332]"    
cpb-aacip-225-27zkh3tm,"[0.13991300745650373, 0.9004195804195805, 0.7714285714285715]","[0.13991300745650373, 0.9004195804195805, 0.7547619047619047]"
cpb-aacip-225-31qftxh5,False,False
cpb-aacip-225-37vmd093,"[0.11377919542336812, 0.25805760187574694, 0.3174639061857107]","[0.11282681447098716, 0.25360625612005333, 0.30758802600907864]"
cpb-aacip-225-44bnzxh7,"[0.23139499250936205, 0.7336274836274835, 0.7146520146520148]","[0.22879758991195942, 0.7336274836274835, 0.7076590076590077]"
cpb-aacip-225-48sbchm7,False,False
cpb-aacip-225-51vdnj5t,"[0.6944250871080138, 0.7647058823529411, 0.0]","[0.008333333333333333, 0.0, 0.0]"
cpb-aacip-225-65v6x41w,"[0.6612903225806451, 0.3181818181818182, 0.6666666666666666]","[0.6612903225806451, 0.3181818181818182, 0.6666666666666666]" 

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
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>245145</td>
      <td>{'name-as-written': 'Ted Liu', 'name-normalized': 'Liu, Ted', 'attributes': ['Director', 'DBEDT']}</td>
      <td>{'name-as-written': 'TED LIU', 'name-normalized': 'Liu, Ted', 'attributes': ['DIRECTOR', 'DBEDT']}</td>
      <td>{'name-as-written': 0.5714285714285714, 'name-normalized': 0.0, 'attributes': 0.5384615384615384}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>640507</td>
      <td>{'name-as-written': 'Mark Sasaki', 'name-normalized': 'Sasaki, Mark', 'attributes': ['Big City Diner']}</td>
      <td>{'name-as-written': 'THE EMPLOYEES STARS', 'name-normalized': 'Employees Stars, The', 'attributes': ['mam', 'MARK SASAKI', 'BIG CITY DINER']}</td>
      <td>{'name-as-written': 0.8947368421052632, 'name-normalized': 0.85, 'attributes': 0.8214285714285714}</td>
      <td>{'name-as-written': 0.7894736842105263, 'name-normalized': 0.8, 'attributes': 0.5}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>105506</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Edition']}</td>
      <td>{'name-as-written': 'a', 'name-normalized': 'A', 'attributes': ['AN tu', 'NETTE LO TOM', 'Hawaii Edition', '22 - - - - -']}</td>
      <td>{'name-as-written': 14.0, 'name-normalized': 15.0, 'attributes': 0.6744186046511628}</td>
      <td>{'name-as-written': 14.0, 'name-normalized': 15.0, 'attributes': 0.6744186046511628}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>202135</td>
      <td>{'name-as-written': 'PHIL ESTERMAN', 'name-normalized': 'Esterman, Phil', 'attributes': ['Save Sandy Beach Coalition']}</td>
      <td>{'name-as-written': 'PHIL', 'name-normalized': 'Phil', 'attributes': ['ESTERMANN', 'kpues uontegoougeeg']}</td>
      <td>{'name-as-written': 2.25, 'name-normalized': 2.5, 'attributes': 0.9285714285714286}</td>
      <td>{'name-as-written': 2.25, 'name-normalized': 2.5, 'attributes': 0.8214285714285714}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>230764</td>
      <td>{'name-as-written': 'STEVE HIRANO', 'name-normalized': 'Hirano, Steve', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'STEVE', 'name-normalized': 'Steve', 'attributes': ['HIRANO', 'p090/510qu619N.290 Planning']}</td>
      <td>{'name-as-written': 1.4, 'name-normalized': 1.6, 'attributes': 0.7272727272727273}</td>
      <td>{'name-as-written': 1.4, 'name-normalized': 1.6, 'attributes': 0.696969696969697}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>248282</td>
      <td>{'name-as-written': 'DONNA GOTH', 'name-normalized': 'Goth, Donna', 'attributes': ['Land Use Research Foundation of Hawaii']}</td>
      <td>{'name-as-written': 'DONNA', 'name-normalized': 'Donna', 'attributes': ['GOTH', 'Land Use Researchfoundation', 'ofHawail']}</td>
      <td>{'name-as-written': 1.0, 'name-normalized': 1.2, 'attributes': 0.23076923076923078}</td>
      <td>{'name-as-written': 1.0, 'name-normalized': 1.2, 'attributes': 0.20512820512820512}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>301001</td>
      <td>{'name-as-written': 'KELLY DEAN', 'name-normalized': 'Dean, Kelly', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'NVEGATTEX', 'name-normalized': 'Nvegattex', 'attributes': ['Hawaii Sugna UOISTAGTEL']}</td>
      <td>{'name-as-written': 1.0, 'name-normalized': 1.1111111111111112, 'attributes': 0.6521739130434783}</td>
      <td>{'name-as-written': 1.0, 'name-normalized': 1.1111111111111112, 'attributes': 0.6521739130434783}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>321522</td>
      <td>{'name-as-written': 'JOANN YUKIMURA (D)', 'name-normalized': 'Yukimura, Joann', 'attributes': ['Kauai Mayor']}</td>
      <td>{'name-as-written': 'NIVOr FENWENA G', 'name-normalized': 'Fenwena G, Nivor', 'attributes': ['Kauail JokeW']}</td>
      <td>{'name-as-written': 1.0, 'name-normalized': 0.875, 'attributes': 0.5}</td>
      <td>{'name-as-written': 1.0, 'name-normalized': 0.875, 'attributes': 0.5}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>360027</td>
      <td>{'name-as-written': 'REP. EZRA KANOHO (D)', 'name-normalized': 'Kanoho, Ezra', 'attributes': ['Lihue/Kapaa']}</td>
      <td>{'name-as-written': '-', 'name-normalized': '-', 'attributes': ['A', 'A', 'EZRA', 'KANOHO 6', 'eedeyenuin']}</td>
      <td>{'name-as-written': 20.0, 'name-normalized': 12.0, 'attributes': 0.9583333333333334}</td>
      <td>{'name-as-written': 20.0, 'name-normalized': 12.0, 'attributes': 0.9166666666666666}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>437504</td>
      <td>{'name-as-written': 'GOV. JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': []}</td>
      <td>{'name-as-written': 'Jan. 31', 'name-normalized': '31', 'attributes': ['PAQ5 JOHN WAIHEE(D)']}</td>
      <td>{'name-as-written': 2.5714285714285716, 'name-normalized': 6.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 2.4285714285714284, 'name-normalized': 6.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>494528</td>
      <td>{'name-as-written': 'GARY GILL', 'name-normalized': 'Gill, Gary', 'attributes': ['Honolulu City Council Member']}</td>
      <td>{'name-as-written': 'GARY', 'name-normalized': 'Gary', 'attributes': ['GILL', 'nnjouof Gitycouncil Member', '-']}</td>
      <td>{'name-as-written': 1.25, 'name-normalized': 1.5, 'attributes': 0.41935483870967744}</td>
      <td>{'name-as-written': 1.25, 'name-normalized': 1.5, 'attributes': 0.3870967741935484}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>532900</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'NHOF ELETEGVE', 'name-normalized': 'Eletegve, Nhof', 'attributes': ['poop/PERENGIYRROD Bupued']}</td>
      <td>{'name-as-written': 0.9230769230769231, 'name-normalized': 0.8571428571428571, 'attributes': 1.0416666666666667}</td>
      <td>{'name-as-written': 0.9230769230769231, 'name-normalized': 0.8571428571428571, 'attributes': 0.9166666666666666}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>598632</td>
      <td>{'name-as-written': 'GARY GILL', 'name-normalized': 'Gill, Gary', 'attributes': ['Honolulu City Council Member']}</td>
      <td>{'name-as-written': 'GARY GILL', 'name-normalized': 'Gill, Gary', 'attributes': ['Honolatu Gly Gouncil Member']}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.2222222222222222}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.2222222222222222}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>640774</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'NHOF EFETOGME', 'name-normalized': 'Efetogme, Nhof', 'attributes': ['Good Netghbors) -', 'GoodPlanning']}</td>        
      <td>{'name-as-written': 0.9230769230769231, 'name-normalized': 0.8571428571428571, 'attributes': 0.1724137931034483}</td>
      <td>{'name-as-written': 0.9230769230769231, 'name-normalized': 0.8571428571428571, 'attributes': 0.1724137931034483}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>884751</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'JOHN FAFTISOVE', 'name-normalized': 'Faftisove, John', 'attributes': ['/STOGUDIONDOOD Good Bupuere']}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 0.4666666666666667, 'attributes': 0.8518518518518519}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 0.4666666666666667, 'attributes': 0.7777777777777778}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1021755</td>
      <td>{'name-as-written': 'MARTHA HULBERT', 'name-normalized': 'Hulbert, Martha', 'attributes': ['Adoption Circle of Hawaii']}</td>
      <td>{'name-as-written': 'MARTHA', 'name-normalized': 'Martha', 'attributes': ['HULBERT', 'tondopy Gircle of Hawail']}</td>
      <td>{'name-as-written': 1.3333333333333333, 'name-normalized': 1.5, 'attributes': 0.45161290322580644}</td>
      <td>{'name-as-written': 1.3333333333333333, 'name-normalized': 1.5, 'attributes': 0.41935483870967744}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1183016</td>
      <td>{'name-as-written': 'VERA BENEDEK', 'name-normalized': 'Benedek, Vera', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'VERA', 'name-normalized': 'Vera', 'attributes': ['BENEDEK', 'Hawaii Public Television']}</td>
      <td>{'name-as-written': 2.0, 'name-normalized': 2.25, 'attributes': 0.22580645161290322}</td>
      <td>{'name-as-written': 2.0, 'name-normalized': 2.25, 'attributes': 0.22580645161290322}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1308141</td>
      <td>{'name-as-written': 'ARTHUR ROSS', 'name-normalized': 'Ross, Arthur', 'attributes': ['Neighborhood Board Chairman']}</td>
      <td>{'name-as-written': 'ENHEY 3033', 'name-normalized': '3033, Enhey', 'attributes': ['pangapouvequeN Ghatrman']}</td>
      <td>{'name-as-written': 0.9, 'name-normalized': 0.8181818181818182, 'attributes': 0.782608695652174}</td>
      <td>{'name-as-written': 0.9, 'name-normalized': 0.8181818181818182, 'attributes': 0.782608695652174}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>96763</td>
      <td>{'name-as-written': 'DAN BOYLAN', 'name-normalized': 'Boylan, Dan', 'attributes': ['Newsmakers']}</td>
      <td>{'name-as-written': 'DAN BOYLAN', 'name-normalized': 'Boylan, Dan', 'attributes': ['Newsmakers']}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>149016</td>
      <td>{'name-as-written': 'WHITNEY ANDERSON (R)', 'name-normalized': 'Anderson, Whitney', 'attributes': ['State Senate Candidate', 'District 25 Kailua, Waimanalo']}</td>
      <td>{'name-as-written': '- I -', 'name-normalized': 'I -, -', 'attributes': ['WHITNEY NOSHIONV (R)', 'State Senate Candidate', 'Distrist 25 Kailua, Waimanalu']}</td>
      <td>{'name-as-written': 3.6, 'name-normalized': 2.5, 'attributes': 0.30985915492957744}</td>
      <td>{'name-as-written': 3.6, 'name-normalized': 2.5, 'attributes': 0.30985915492957744}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>312779</td>
      <td>{'name-as-written': 'FRED HEMMINGS (R)', 'name-normalized': 'Hemmings, Fred', 'attributes': ['State Senate Candidate', 'District 25 Kailua, Waimanalo']}</td>
      <td>{'name-as-written': 'FRED HEMMINGS (R)', 'name-normalized': 'Hemmings, Fred', 'attributes': ['State Senate Candidate', 'District SC Kailua, Waimanale']}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.058823529411764705}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.058823529411764705}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>933767</td>
      <td>{'name-as-written': 'ALEX SONSON (D)', 'name-normalized': 'Sonson, Alex', 'attributes': ['State Rep. Candidate', 'District 36 Pearl City, Waipahu']}</td>
      <td>{'name-as-written': 'ALEX NOSNOS @', 'name-normalized': 'Nosnos @, Alex', 'attributes': ['SIBIS $ Candidate', 'District 95 Pearl Chy, Waipainu']}</td>
      <td>{'name-as-written': 0.5384615384615384, 'name-normalized': 0.35714285714285715, 'attributes': 0.2916666666666667}</td>
      <td>{'name-as-written': 0.5384615384615384, 'name-normalized': 0.35714285714285715, 'attributes': 0.2916666666666667}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>985652</td>
      <td>{'name-as-written': 'ROY TAKUMI (D)', 'name-normalized': 'Takumi, Roy', 'attributes': ['State Rep. Candidate', 'District 36 Pearl City, Waipahu']}</td>
      <td>{'name-as-written': 'ROYTAKUMI 9', 'name-normalized': '9, Roytakumi', 'attributes': ['State Rep. Candidate', 'District 99 Pearl City, Waipahu']}</td>
      <td>{'name-as-written': 0.36363636363636365, 'name-normalized': 1.0, 'attributes': 0.0392156862745098}</td>
      <td>{'name-as-written': 0.36363636363636365, 'name-normalized': 0.9166666666666666, 'attributes': 0.0392156862745098}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>88889</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Lo Tom, Lynette', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.4, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.4, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>119253</td>
      <td>{'name-as-written': 'JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': ['Governor']}</td>
      <td>{'name-as-written': 'JOHN ACHIVA (D)', 'name-normalized': 'Achiva, John', 'attributes': ['Governor']}</td>
      <td>{'name-as-written': 0.3333333333333333, 'name-normalized': 0.5, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.3333333333333333, 'name-normalized': 0.4166666666666667, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>174775</td>
      <td>{'name-as-written': 'Rep. SAMUEL LEE (D)', 'name-normalized': 'Lee, Samuel', 'attributes': ['Vice Chairman', 'House Education Committee']}</td>
      <td>{'name-as-written': 'Rep. SAMUEL LEE (D', 'name-normalized': 'Lee, Samuel', 'attributes': ['Vice Chairman', 'House Education Committee']}</td>
      <td>{'name-as-written': 0.05555555555555555, 'name-normalized': 0.0, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.05555555555555555, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>185886</td>
      <td>{'name-as-written': 'Sen. BERTRAND KOBAYASHI (D)', 'name-normalized': 'Kobayashi, Bertrand', 'attributes': ['Chairman, Senate Education Committee']}</td>
      <td>{'name-as-written': 'ues BERTRAND', 'name-normalized': 'Bertrand, Ues', 'attributes': ['KOBAYASHI', 'D)', 'Chairman, Senate Education Committee']}</td>
      <td>{'name-as-written': 1.4166666666666667, 'name-normalized': 1.1538461538461537, 'attributes': 0.23404255319148937}</td>
      <td>{'name-as-written': 1.4166666666666667, 'name-normalized': 1.1538461538461537, 'attributes': 0.23404255319148937}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>214281</td>
      <td>{'name-as-written': 'Rep. ROD TAM (D)', 'name-normalized': 'Tam, Rod', 'attributes': ['Chairman', 'House Education Committee']}</td>       
      <td>{'name-as-written': 'Rep ROD TAM D', 'name-normalized': 'Rod Tam D, Rep', 'attributes': ['Chairman', 'House Education Committee']}</td>    
      <td>{'name-as-written': 0.23076923076923078, 'name-normalized': 0.5714285714285714, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.23076923076923078, 'name-normalized': 0.5714285714285714, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>255255</td>
      <td>{'name-as-written': 'Rep. BOB McEACHERN', 'name-normalized': 'McEachern, Bob', 'attributes': ['Minnesota Legislator']}</td>
      <td>{'name-as-written': 'Rep.BOB MGEACHERN', 'name-normalized': 'Mgeachern, Bob', 'attributes': ['Minnesota', 'Legislator']}</td>
      <td>{'name-as-written': 0.11764705882352941, 'name-normalized': 0.14285714285714285, 'attributes': 0.05263157894736842}</td>
      <td>{'name-as-written': 0.11764705882352941, 'name-normalized': 0.07142857142857142, 'attributes': 0.05263157894736842}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>295529</td>
      <td>{'name-as-written': 'Sen. MIKE McCARTNEY (D)', 'name-normalized': 'McCartney, Mike', 'attributes': ['Vice Chairman', 'Senate Education Committee']}</td>
      <td>{'name-as-written': 'Sen. MIKE MCGARTNEY (D)', 'name-normalized': 'Mcgartney, Mike', 'attributes': ['Vice Chairman', 'Senate Education Committee']}</td>
      <td>{'name-as-written': 0.08695652173913043, 'name-normalized': 0.06666666666666667, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.043478260869565216, 'name-normalized': 0.06666666666666667, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>414281</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Lo Tom, Lynette', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.4, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.4, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>447648</td>
      <td>{'name-as-written': 'EVAN THOMAS', 'name-normalized': 'Thomas, Evan', 'attributes': ['Common Cause']}</td>
      <td>{'name-as-written': 'BAN THOMAS', 'name-normalized': 'Thomas, Ban', 'attributes': ['Common Cause']}</td>
      <td>{'name-as-written': 0.2, 'name-normalized': 0.18181818181818182, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.2, 'name-normalized': 0.18181818181818182, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>461128</td>
      <td>{'name-as-written': 'PATSY T. MINK', 'name-normalized': 'Mink, Patsy T.', 'attributes': ['The Public Reporter']}</td>
      <td>{'name-as-written': 'PATSY UC MINK', 'name-normalized': 'Uc Mink, Patsy', 'attributes': ['The Public 1311oday']}</td>
      <td>{'name-as-written': 0.15384615384615385, 'name-normalized': 0.42857142857142855, 'attributes': 0.42105263157894735}</td>
      <td>{'name-as-written': 0.15384615384615385, 'name-normalized': 0.42857142857142855, 'attributes': 0.42105263157894735}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>520521</td>
      <td>{'name-as-written': 'Sen. MARY GEORGE (R)', 'name-normalized': 'George, Mary', 'attributes': ['Senate Minority Leader']}</td>
      <td>{'name-as-written': 'sen. MARY GEORGE (R)', 'name-normalized': 'George, Mary', 'attributes': ['Senate Minority Leader']}</td>
      <td>{'name-as-written': 0.05, 'name-normalized': 0.0, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>546380</td>
      <td>{'name-as-written': 'Rep. PETER APO (D)', 'name-normalized': 'Apo, Peter', 'attributes': ['House Majority Floor Leader']}</td>
      <td>{'name-as-written': 'Rep. PETER APO U', 'name-normalized': 'Apo U, Peter', 'attributes': ['House Majority-Floor Leader']}</td>
      <td>{'name-as-written': 0.1875, 'name-normalized': 0.16666666666666666, 'attributes': 0.037037037037037035}</td>
      <td>{'name-as-written': 0.1875, 'name-normalized': 0.16666666666666666, 'attributes': 0.037037037037037035}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>607007</td>
      <td>{'name-as-written': 'JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': ['Governor']}</td>
      <td>{'name-as-written': 'NHOT WAIHEE a', 'name-normalized': 'Waihee A, Nhot', 'attributes': ['lou.13105']}</td>
      <td>{'name-as-written': 0.5384615384615384, 'name-normalized': 0.42857142857142855, 'attributes': 0.8888888888888888}</td>
      <td>{'name-as-written': 0.5384615384615384, 'name-normalized': 0.42857142857142855, 'attributes': 0.8888888888888888}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>647014</td>
      <td>{'name-as-written': 'Rep. ROLAND KOTANI (D)', 'name-normalized': 'Kotani, Roland', 'attributes': ['Pearl City/Pacific Palisades']}</td>    
      <td>{'name-as-written': 'Rep. INVTOU KOTANT (D)', 'name-normalized': 'Kotant, Invtou', 'attributes': ['Pearl Gity/Pacitic Palisades']}</td>    
      <td>{'name-as-written': 0.3181818181818182, 'name-normalized': 0.5, 'attributes': 0.07142857142857142}</td>
      <td>{'name-as-written': 0.3181818181818182, 'name-normalized': 0.5, 'attributes': 0.07142857142857142}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>677010</td>
      <td>{'name-as-written': 'Sen. ELOISE TUNGPALAN (D)', 'name-normalized': 'Tungpalan, Eloise', 'attributes': ['Chairman, Senate Culture & Arts Committee']}</td>
      <td>{'name-as-written': 'Sen. ELOISE ANTVONNIA D', 'name-normalized': 'Antvonnia D, Eloise', 'attributes': ['Chairman, Senate. Culture', '2 Arts Committee']}</td>
      <td>{'name-as-written': 0.4782608695652174, 'name-normalized': 0.5263157894736842, 'attributes': 0.07317073170731707}</td>
      <td>{'name-as-written': 0.4782608695652174, 'name-normalized': 0.47368421052631576, 'attributes': 0.07317073170731707}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>778779</td>
      <td>{'name-as-written': 'Sen. RICK REED (R)', 'name-normalized': 'Reed, Rick', 'attributes': ['Senate Minority Floor Leader']}</td>
      <td>{'name-as-written': 'Sen. RICK REED (R)', 'name-normalized': 'Reed, Rick', 'attributes': ['Senate Minority Floor Leader']}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>800400</td>
      <td>{'name-as-written': 'Sen. GERALD HAGINO (D)', 'name-normalized': 'Hagino, Gerald', 'attributes': ['Senate Majority Leader']}</td>
      <td>{'name-as-written': 'Sen. GERALD HAGINO (D)', 'name-normalized': 'Hagino, Gerald', 'attributes': ['Senate Majority Leader']}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>849516</td>
      <td>{'name-as-written': 'Sen. RUSSELL BLAIR (D)', 'name-normalized': 'Blair, Russell', 'attributes': ['Senate Majority Floor Leader']}</td>    
      <td>{'name-as-written': 'Sen. TTESSN BLAIR D', 'name-normalized': 'Blair D, Ttessn', 'attributes': ['Senate Majority Floor Leader']}</td>      
      <td>{'name-as-written': 0.42105263157894735, 'name-normalized': 0.5333333333333333, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.42105263157894735, 'name-normalized': 0.5333333333333333, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>948782</td>
      <td>{'name-as-written': 'Rep. DWIGHT TAKAMINE (D)', 'name-normalized': 'Takamine, Dwight', 'attributes': ['North Hilo/Hamakua']}</td>
      <td>{'name-as-written': 'Rep. DWIGHT TAKAMINE (D', 'name-normalized': 'Takamine, Dwight', 'attributes': ['North Hilo/Hamakua']}</td>
      <td>{'name-as-written': 0.043478260869565216, 'name-normalized': 0.0, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.043478260869565216, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>1080013</td>
      <td>{'name-as-written': 'Rep. DAVID IGE (D)', 'name-normalized': 'Ige, David', 'attributes': ['Chairman, Economic Dev. & Hawaiian Affairs Com.']}</td>
      <td>{'name-as-written': 'Rep. DAVID IGE @', 'name-normalized': 'Ige @, David', 'attributes': ['Chairman, Economic Dex', '8 Hawaiian Affairs Gom.']}</td>
      <td>{'name-as-written': 0.1875, 'name-normalized': 0.16666666666666666, 'attributes': 0.1111111111111111}</td>
      <td>{'name-as-written': 0.1875, 'name-normalized': 0.16666666666666666, 'attributes': 0.1111111111111111}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>1295028</td>
      <td>{'name-as-written': 'Sen. LEHUA FERNANDES SALLING (D)', 'name-normalized': 'Fernandes Salling, Lehua', 'attributes': ['Chairman', 'Senate Transportation Committee']}</td>
      <td>{'name-as-written': 'Sen. LEHUA FERNANDES', 'name-normalized': 'Fernandes, Lehua', 'attributes': ['ONFITYS (D)', 'Chairman', 'Senate uonejsodsueIL Committee', '*']}</td>
      <td>{'name-as-written': 0.6, 'name-normalized': 0.5, 'attributes': 0.5}</td>
      <td>{'name-as-written': 0.6, 'name-normalized': 0.5, 'attributes': 0.48}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>108275</td>
      <td>{'name-as-written': 'LESLIE WILCOX', 'name-normalized': 'Wilcox, Leslie', 'attributes': ['ELECTION LIVE']}</td>
      <td>{'name-as-written': 'LESLIE XOOTIM', 'name-normalized': 'Xootim, Leslie', 'attributes': ['ELECTION LIVE']}</td>
      <td>{'name-as-written': 0.46153846153846156, 'name-normalized': 0.42857142857142855, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.46153846153846156, 'name-normalized': 0.42857142857142855, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>270904</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Former Congressional Candidate']}</td>
      <td>{'name-as-written': 'NHOP RADGLIFFE', 'name-normalized': 'Radgliffe, Nhop', 'attributes': ['Former Congressional Candidate']}</td>
      <td>{'name-as-written': 0.35714285714285715, 'name-normalized': 0.3333333333333333, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.35714285714285715, 'name-normalized': 0.3333333333333333, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>347514</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Keir, Gerry', 'attributes': ['Managing Editor', 'Honolulu Advertiser']}</td>
      <td>{'name-as-written': 'GERRY KER', 'name-normalized': 'Ker, Gerry', 'attributes': ['a', 'u', 'Managing Editor', 'a Monolokabberitor']}</td>  
      <td>{'name-as-written': 0.1111111111111111, 'name-normalized': 0.1, 'attributes': 0.42857142857142855}</td>
      <td>{'name-as-written': 0.1111111111111111, 'name-normalized': 0.1, 'attributes': 0.4}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>422756</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Former Congressional Candidate']}</td>
      <td>{'name-as-written': 'NHOT RADCLIFFE', 'name-normalized': 'Radcliffe, Nhot', 'attributes': ['Former Congressional Candidate,']}</td>        
      <td>{'name-as-written': 0.2857142857142857, 'name-normalized': 0.26666666666666666, 'attributes': 0.03225806451612903}</td>
      <td>{'name-as-written': 0.2857142857142857, 'name-normalized': 0.26666666666666666, 'attributes': 0.03225806451612903}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>488522</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Keir, Gerry', 'attributes': ['Managing Editor', 'Honolulu Advertiser']}</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Keir, Gerry', 'attributes': ['Managing = Editor', 'Honolulu Advertiser']}</td>       
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.05555555555555555}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.05555555555555555}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>784151</td>
      <td>{'name-as-written': 'NINA BERGLUND', 'name-normalized': 'Berglund, Nina', 'attributes': ['Election Live']}</td>
      <td>{'name-as-written': '215', 'name-normalized': '215', 'attributes': ['SERASTALISE Guguads', 'OFFICE OFTHE', 'UEUTENANT GOVERNOR', 'NINA GNNTREES', 'Election Live']}</td>
      <td>{'name-as-written': 4.333333333333333, 'name-normalized': 4.666666666666667, 'attributes': 0.8266666666666667}</td>
      <td>{'name-as-written': 4.333333333333333, 'name-normalized': 4.666666666666667, 'attributes': 0.8266666666666667}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>801635</td>
      <td>{'name-as-written': 'DAN TUTTLE', 'name-normalized': 'Tuttle, Dan', 'attributes': ['Political Analyst']}</td>
      <td>{'name-as-written': 'DAN ETIJOL -', 'name-normalized': 'Etijol -, Dan', 'attributes': ['Political Analyst']}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 0.5384615384615384, 'attributes': 0.0}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 0.46153846153846156, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>830030</td>
      <td>{'name-as-written': 'ANDREW POEPOE', 'name-normalized': 'Poepoe, Andrew', 'attributes': ['Co-Chairman', 'Saiki in '88 Committee']}</td>    
      <td>{'name-as-written': 'ANDREW B0d30d', 'name-normalized': 'B0d30d, Andrew', 'attributes': ['Co-Chairman,', 'Saikiin 88. Committee']}</td>    
      <td>{'name-as-written': 0.46153846153846156, 'name-normalized': 0.42857142857142855, 'attributes': 0.12121212121212122}</td>
      <td>{'name-as-written': 0.46153846153846156, 'name-normalized': 0.42857142857142855, 'attributes': 0.12121212121212122}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1068902</td>
      <td>{'name-as-written': 'STAN KOKI (R)', 'name-normalized': 'Koki, Stan', 'attributes': []}</td>
      <td>{'name-as-written': 'STAN KOKI (R)', 'name-normalized': 'Koki, Stan', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1183016</td>
      <td>{'name-as-written': 'CLAYTON HEE (D)', 'name-normalized': 'Hee, Clayton', 'attributes': []}</td>
      <td>{'name-as-written': 'CLAYTON', 'name-normalized': 'Clayton', 'attributes': ['HEE', '(D)']}</td>
      <td>{'name-as-written': 1.1428571428571428, 'name-normalized': 0.7142857142857143, 'attributes': 1.0}</td>
      <td>{'name-as-written': 1.1428571428571428, 'name-normalized': 0.7142857142857143, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1417150</td>
      <td>{'name-as-written': 'JERRY BURRIS', 'name-normalized': 'Burris, Jerry', 'attributes': ['Politics Editor', 'Honolulu Advertiser']}</td>     
      <td>{'name-as-written': 'Aadar BURRIS', 'name-normalized': 'Burris, Aadar', 'attributes': ['Politics Edittor', 'Honolulu Advertiser -']}</td>  
      <td>{'name-as-written': 0.4166666666666667, 'name-normalized': 0.38461538461538464, 'attributes': 0.08108108108108109}</td>
      <td>{'name-as-written': 0.4166666666666667, 'name-normalized': 0.38461538461538464, 'attributes': 0.08108108108108109}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>99766</td>
      <td>{'name-as-written': 'Howard Dicus', 'name-normalized': 'Dicus, Howard', 'attributes': ['PBN Friday']}</td>
      <td>{'name-as-written': 'HOWARD DICUS', 'name-normalized': 'Dicus, Howard', 'attributes': ['PBN FRIDAY']}</td>
      <td>{'name-as-written': 0.75, 'name-normalized': 0.0, 'attributes': 0.5}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>286753</td>
      <td>{'name-as-written': 'Connie Lau', 'name-normalized': 'Lau, Connie', 'attributes': ['CEO', 'American Savings Bank']}</td>
      <td>{'name-as-written': 'CONNIE LAU', 'name-normalized': 'Lau, Connie', 'attributes': ['CEO', 'AMERICAN SAVINGS BANK']}</td>
      <td>{'name-as-written': 0.7, 'name-normalized': 0.0, 'attributes': 0.6666666666666666}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>644878</td>
      <td>{'name-as-written': 'Sterling Paulos', 'name-normalized': 'Paulos, Sterling', 'attributes': ['Hotel Director', 'NCL Hawaii']}</td>
      <td>{'name-as-written': 'STERLING PAULOS', 'name-normalized': 'Paulos, Sterling', 'attributes': ['HOTEL DIRECTOR', 'NCL HAWAIL']}</td>
      <td>{'name-as-written': 0.8, 'name-normalized': 0.0, 'attributes': 0.6666666666666666}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.041666666666666664}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>954521</td>
      <td>{'name-as-written': 'Susan Todani', 'name-normalized': 'Todani, Susan', 'attributes': ['Director of Investments', 'Kamehameha Schools']}</td>
      <td>{'name-as-written': 'SUSAN TODANI', 'name-normalized': 'Todani, Susan', 'attributes': ['DIRECTOR OF INVESTMENTS', 'KAMEHAMEHA SCHOOLS']}</td>
      <td>{'name-as-written': 0.75, 'name-normalized': 0.0, 'attributes': 0.8292682926829268}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>1032032</td>
      <td>{'name-as-written': 'Rosalind Schurgin', 'name-normalized': 'Schurgin, Rosalind', 'attributes': ['Executive Vice President', 'Festival Companies']}</td>
      <td>{'name-as-written': 'ROSALIND SCHURGIN', 'name-normalized': 'Schurgin, Rosalind', 'attributes': ['EXECUTIVE VICE PRESIDENT', 'FESTIVAL COMPANIES']}</td>
      <td>{'name-as-written': 0.8235294117647058, 'name-normalized': 0.0, 'attributes': 0.8095238095238095}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-65v6x41w (18 rows)</td>
      <td>250150</td>
      <td>{'name-as-written': 'CHARLES TOGUCHI', 'name-normalized': 'Toguchi, Charles', 'attributes': ['Superintendent', 'Dept. of Education']}</td> 
      <td>{'name-as-written': 'CHARLES TOGUCHI', 'name-normalized': 'Toguchi, Charles', 'attributes': ['Superintendent', 'Depto of yoneonpa']}</td>  
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.3225806451612903}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 0.0, 'attributes': 0.3225806451612903}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-65v6x41w (18 rows)</td>
      <td>1179646</td>
      <td>{'name-as-written': 'Rep. DANIEL KIHANO', 'name-normalized': 'Kihano, Daniel', 'attributes': []}</td>
      <td>{'name-as-written': 'Rep. DANIEL', 'name-normalized': 'Daniel', 'attributes': ['KIHANO']}</td>
      <td>{'name-as-written': 0.6363636363636364, 'name-normalized': 1.3333333333333333, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6363636363636364, 'name-normalized': 1.3333333333333333, 'attributes': 1.0}</td>
    </tr>
  </tbody>
</table>

## Data specs
- Groundtruth data location: KeyedInformationExtraction/golds_test'
- System prediction (MMIF) location: KeyedInformationExtraction/smol_preds'

## Pipeline specs

## Raw Results
```
GUID,mean-CER-cased,mean-CER-uncased
cpb-aacip-225-12z34w2c,"[0.5714285714285714, 0.4362874158640749, 1.0]","[0.5714285714285714, 0.3622856412411823, 1.0]"
cpb-aacip-225-15bcc3x8,"[1.0, 0.7922705314009661, 1.0]","[1.0, 0.644122383252818, 1.0]"
cpb-aacip-225-20ftth6f,"[0.9375, 0.7073430768469411, 1.0]","[0.9375, 0.6369090490691633, 1.0]"
cpb-aacip-225-27zkh3tm,"[1.0, 0.7554327064927567, 1.0]","[1.0, 0.7198162681365924, 1.0]"
cpb-aacip-225-31qftxh5,"[1.0, 0.5597972972972973, 1.0]","[1.0, 0.5597972972972973, 1.0]"
cpb-aacip-225-37vmd093,"[1.0, 0.6567170618906852, 1.0]","[1.0, 0.5719607468420644, 1.0]"
cpb-aacip-225-44bnzxh7,"[0.8181818181818182, 0.6372298104194656, 1.0]","[0.8181818181818182, 0.5633381848037021, 1.0]"
cpb-aacip-225-48sbchm7,"[0.6, 0.5555244755244756, 1.0]","[0.6, 0.4242424242424242, 1.0]"
cpb-aacip-225-51vdnj5t,"[1.0, 0.7724835344174391, 1.0]","[1.0, 0.6815274620660178, 1.0]"
cpb-aacip-225-65v6x41w,"[0.5, 0.47058823529411764, 1.0]","[0.5, 0.3627450980392157, 1.0]"

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
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>188155</td>
      <td>{'name-as-written': 'GEORGE TAKANE', 'name-normalized': 'Takane, George', 'attributes': ['HOUSE CLERK']}</td>
      <td>{'name-as-written': 'GEORGE TAKANE CLERK', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.3157894736842105, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.3157894736842105, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>525759</td>
      <td>{'name-as-written': 'JAY LARRIN', 'name-normalized': 'Larrin, Jay', 'attributes': []}</td>
      <td>{'name-as-written': 'JAY LARRIN, M.D.', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.375, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.375, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>686019</td>
      <td>{'name-as-written': 'LOYAL GARNER', 'name-normalized': 'Garner, Loyal', 'attributes': []}</td>
      <td>{'name-as-written': 'LOYAL GARNER', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>701268</td>
      <td>{'name-as-written': 'RICHARD S. H. WONG', 'name-normalized': 'Wong, Richard S. H.', 'attributes': ['SENATE PRESIDENT']}</td>
      <td>{'name-as-written': 'Richard S.H. Wong, Senate President', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5428571428571428, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>790390</td>
      <td>{'name-as-written': 'REV. WILLIAM KAINA', 'name-normalized': 'Kaina, William', 'attributes': []}</td>
      <td>{'name-as-written': 'REV. WILLIAM KAINAA', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.05263157894736842, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.05263157894736842, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>1000400</td>
      <td>{'name-as-written': 'DAVID WOO', 'name-normalized': 'Woo, David', 'attributes': ['SENATE CLERK']}</td>
      <td>{'name-as-written': 'David Woo, Senate Clerk', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8695652173913043, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6086956521739131, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-12z34w2c (13 rows)</td>
      <td>1176009</td>
      <td>{'name-as-written': 'STACY SAKAMOTO', 'name-normalized': 'Sakamoto, Stacy', 'attributes': ['HAWAII PUBLIC TELEVISION']}</td>
      <td>{'name-as-written': 'STACY SAKAMOTO HAWAII PUBLIC TELEVISION', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6410256410256411, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6410256410256411, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>245145</td>
      <td>{'name-as-written': 'Ted Liu', 'name-normalized': 'Liu, Ted', 'attributes': ['Director', 'DBEDT']}</td>
      <td>{'name-as-written': 'Ted Liu, Director, DBDT', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6956521739130435, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6956521739130435, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-15bcc3x8 (4 rows)</td>
      <td>640507</td>
      <td>{'name-as-written': 'Mark Sasaki', 'name-normalized': 'Sasaki, Mark', 'attributes': ['Big City Diner']}</td>
      <td>{'name-as-written': 'MARK SASAKI, BIG CITY DINER', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8888888888888888, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5925925925925926, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>105506</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Edition']}</td>
      <td>{'name-as-written': 'LYNETTE LO TOM, HAWAII EDITION', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5333333333333333, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5333333333333333, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>202135</td>
      <td>{'name-as-written': 'PHIL ESTERMAN', 'name-normalized': 'Esterman, Phil', 'attributes': ['Save Sandy Beach Coalition']}</td>
      <td>{'name-as-written': 'PHIL ESTERMANN, SAVE SANDY BEACH COALITION', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6904761904761905, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6904761904761905, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>230764</td>
      <td>{'name-as-written': 'STEVE HIRANO', 'name-normalized': 'Hirano, Steve', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'STEVE HIRANO, Good Neighbors/Good Planning', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7142857142857143, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7142857142857143, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>248282</td>
      <td>{'name-as-written': 'DONNA GOTH', 'name-normalized': 'Goth, Donna', 'attributes': ['Land Use Research Foundation of Hawaii']}</td>
      <td>{'name-as-written': 'Donna Goth, Land Use Research Foundation of Hawaii', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.92, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.8, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>301001</td>
      <td>{'name-as-written': 'KELLY DEAN', 'name-normalized': 'Dean, Kelly', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'Kelly Dean, Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9166666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7222222222222222, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>321522</td>
      <td>{'name-as-written': 'JOANN YUKIMURA (D)', 'name-normalized': 'Yukimura, Joann', 'attributes': ['Kauai Mayor']}</td>
      <td>{'name-as-written': 'Joann YukiMura (D) - Kauai Mayor', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.75, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.4375, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>360027</td>
      <td>{'name-as-written': 'REP. EZRA KANOHO (D)', 'name-normalized': 'Kanoho, Ezra', 'attributes': ['Lihue/Kapaa']}</td>
      <td>{'name-as-written': 'EZRA KANOHO (D) Lihue/Kapa'a', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6428571428571429, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6428571428571429, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>437504</td>
      <td>{'name-as-written': 'GOV. JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': []}</td>
      <td>{'name-as-written': 'Gov. John Waihee (D)', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>494528</td>
      <td>{'name-as-written': 'GARY GILL', 'name-normalized': 'Gill, Gary', 'attributes': ['Honolulu City Council Member']}</td>
      <td>{'name-as-written': 'GARY GILL, Honolulu City Council Member', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7692307692307693, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7692307692307693, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>532900</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE Good Neighbors / Good Planning', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>598632</td>
      <td>{'name-as-written': 'GARY GILL', 'name-normalized': 'Gill, Gary', 'attributes': ['Honolulu City Council Member']}</td>
      <td>{'name-as-written': 'GARY GILL, Homolulu City Council Member', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7692307692307693, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7692307692307693, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>640774</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE Good Neighbors Good Planning', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6744186046511628, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6744186046511628, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>884751</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Good Neighbors/Good Planning']}</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE Good Neighbors / Good Planning', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1021755</td>
      <td>{'name-as-written': 'MARTHA HULBERT', 'name-normalized': 'Hulbert, Martha', 'attributes': ['Adoption Circle of Hawaii']}</td>
      <td>{'name-as-written': 'MARTHA HULBERT, Adoption Circle of Hawaii', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6585365853658537, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6585365853658537, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1183016</td>
      <td>{'name-as-written': 'VERA BENEDEK', 'name-normalized': 'Benedek, Vera', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'VERA BENEDEK Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6756756756756757, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6756756756756757, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-20ftth6f (29 rows)</td>
      <td>1308141</td>
      <td>{'name-as-written': 'ARTHUR ROSS', 'name-normalized': 'Ross, Arthur', 'attributes': ['Neighborhood Board Chairman']}</td>
      <td>{'name-as-written': 'ARTHUR ROSS, Neighborhood Board Chairman', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.725, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.725, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>96763</td>
      <td>{'name-as-written': 'DAN BOYLAN', 'name-normalized': 'Boylan, Dan', 'attributes': ['Newsmakers']}</td>
      <td>{'name-as-written': 'DAN BOYLAN, Newsmakers', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5454545454545454, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5454545454545454, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>149016</td>
      <td>{'name-as-written': 'WHITNEY ANDERSON (R)', 'name-normalized': 'Anderson, Whitney', 'attributes': ['State Senate Candidate', 'District 25 Kailua, Waimanalo']}</td>
      <td>{'name-as-written': 'Whitney Anderson (R) State Senate Candidate District 25 Kailua, Waimanalo', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9041095890410958, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.726027397260274, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>312779</td>
      <td>{'name-as-written': 'FRED HEMMINGS (R)', 'name-normalized': 'Hemmings, Fred', 'attributes': ['State Senate Candidate', 'District 25 Kailua, Waimanalo']}</td>
      <td>{'name-as-written': 'FRED HEMMINGS (R) State Senate Candidate District 25 Kailua, Waimanalo', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7571428571428571, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7571428571428571, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>933767</td>
      <td>{'name-as-written': 'ALEX SONSON (D)', 'name-normalized': 'Sonson, Alex', 'attributes': ['State Rep. Candidate', 'District 36 Pearl City, Waipahu']}</td>
      <td>{'name-as-written': 'ALEX SONSON (D) State Rep. Candidate District 36 Pearl City, Waipahu', 'name-normalized': '', 'attributes': []}</td>  
      <td>{'name-as-written': 0.7794117647058824, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7794117647058824, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-27zkh3tm (5 rows)</td>
      <td>985652</td>
      <td>{'name-as-written': 'ROY TAKUMI (D)', 'name-normalized': 'Takumi, Roy', 'attributes': ['State Rep. Candidate', 'District 36 Pearl City, Waipahu']}</td>
      <td>{'name-as-written': 'ROY TAKUMI (D) State Rep. Candidate District 36 Pearl City, Waipahu', 'name-normalized': '', 'attributes': []}</td>   
      <td>{'name-as-written': 0.7910447761194029, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7910447761194029, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-31qftxh5 (6 rows)</td>
      <td>824391</td>
      <td>{'name-as-written': 'Joseph M. Souki (D)', 'name-normalized': 'Souki, Joseph M.', 'attributes': ['Speaker of the House']}</td>
      <td>{'name-as-written': 'Joseph M. Souki (D) Speaker of the House', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.525, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.525, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-31qftxh5 (6 rows)</td>
      <td>993126</td>
      <td>{'name-as-written': 'Tom Okamura (D)', 'name-normalized': 'Okamura, Tom', 'attributes': ['House Majority Leader']}</td>
      <td>{'name-as-written': 'Tom Okamura (D) House Majority Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5945945945945946, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5945945945945946, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>88889</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'LYNETTE LO TOM, Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.65, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.65, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>119253</td>
      <td>{'name-as-written': 'JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': ['Governor']}</td>
      <td>{'name-as-written': 'JOHN WAIIHEE (D) Governor', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.4, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.4, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>174775</td>
      <td>{'name-as-written': 'Rep. SAMUEL LEE (D)', 'name-normalized': 'Lee, Samuel', 'attributes': ['Vice Chairman', 'House Education Committee']}</td>
      <td>{'name-as-written': 'Rep. SAMUEL LEE (D) Vice Chairman House Education Committee', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6779661016949152, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6779661016949152, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>185886</td>
      <td>{'name-as-written': 'Sen. BERTRAND KOBAYASHI (D)', 'name-normalized': 'Kobayashi, Bertrand', 'attributes': ['Chairman, Senate Education Committee']}</td>
      <td>{'name-as-written': 'Sen. Bertrand Kobayashi (D)', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5555555555555556, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>214281</td>
      <td>{'name-as-written': 'Rep. ROD TAM (D)', 'name-normalized': 'Tam, Rod', 'attributes': ['Chairman', 'House Education Committee']}</td>       
      <td>{'name-as-written': 'Rep. ROD TAM (D) Chairman House Education Committee', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6862745098039216, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6862745098039216, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>255255</td>
      <td>{'name-as-written': 'Rep. BOB McEACHERN', 'name-normalized': 'McEachern, Bob', 'attributes': ['Minnesota Legislator']}</td>
      <td>{'name-as-written': 'Rep. Bob McAhern, Minnesota Legislator', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7631578947368421, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.631578947368421, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>295529</td>
      <td>{'name-as-written': 'Sen. MIKE McCARTNEY (D)', 'name-normalized': 'McCartney, Mike', 'attributes': ['Vice Chairman', 'Senate Education Committee']}</td>
      <td>{'name-as-written': 'MIKE McCARTNEY (D) Vice Chairman Senate Education Committee', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7796610169491526, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7796610169491526, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>414281</td>
      <td>{'name-as-written': 'LYNETTE LO TOM', 'name-normalized': 'Tom, Lynette Lo', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'LYNETTE LO TOM, Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.65, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.65, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>447648</td>
      <td>{'name-as-written': 'EVAN THOMAS', 'name-normalized': 'Thomas, Evan', 'attributes': ['Common Cause']}</td>
      <td>{'name-as-written': 'Evan Thomas, Common Cause', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.88, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.56, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>461128</td>
      <td>{'name-as-written': 'PATSY T. MINK', 'name-normalized': 'Mink, Patsy T.', 'attributes': ['The Public Reporter']}</td>
      <td>{'name-as-written': 'Patsy T. Mink, The Public Reporter', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8235294117647058, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6176470588235294, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>520521</td>
      <td>{'name-as-written': 'Sen. MARY GEORGE (R)', 'name-normalized': 'George, Mary', 'attributes': ['Senate Minority Leader']}</td>
      <td>{'name-as-written': 'Sen. MARY GEORGE (R) Senate Minority Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5348837209302325, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5348837209302325, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>546380</td>
      <td>{'name-as-written': 'Rep. PETER APO (D)', 'name-normalized': 'Apo, Peter', 'attributes': ['House Majority Floor Leader']}</td>
      <td>{'name-as-written': 'Rep. PETER APO (D) House Majority Floor Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6086956521739131, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6086956521739131, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>607007</td>
      <td>{'name-as-written': 'JOHN WAIHEE (D)', 'name-normalized': 'Waihee, John', 'attributes': ['Governor']}</td>
      <td>{'name-as-written': 'JOHN WAIIHEE (D) Governor', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.4, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.4, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>647014</td>
      <td>{'name-as-written': 'Rep. ROLAND KOTANI (D)', 'name-normalized': 'Kotani, Roland', 'attributes': ['Pearl City/Pacific Palisades']}</td>    
      <td>{'name-as-written': 'Rep. ROLAND KOTANI (D) Pearl City/Pacific Palisades', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5686274509803921, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5686274509803921, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>677010</td>
      <td>{'name-as-written': 'Sen. ELOISE TUNGPALAN (D)', 'name-normalized': 'Tungpalan, Eloise', 'attributes': ['Chairman, Senate Culture & Arts Committee']}</td>
      <td>{'name-as-written': 'Sen. ELOISE TUNGPANAL (D) Chairperson, Senate Culture & Arts Committee', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6714285714285714, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6714285714285714, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>778779</td>
      <td>{'name-as-written': 'Sen. RICK REED (R)', 'name-normalized': 'Reed, Rick', 'attributes': ['Senate Minority Floor Leader']}</td>
      <td>{'name-as-written': 'Sen. RICK REED (R) Senate Minority Floor Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6170212765957447, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6170212765957447, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>800400</td>
      <td>{'name-as-written': 'Sen. GERALD HAGINO (D)', 'name-normalized': 'Hagino, Gerald', 'attributes': ['Senate Majority Leader']}</td>
      <td>{'name-as-written': 'Sen. Gerald Hagino (D) Senate Majority Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7333333333333333, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5111111111111111, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>849516</td>
      <td>{'name-as-written': 'Sen. RUSSELL BLAIR (D)', 'name-normalized': 'Blair, Russell', 'attributes': ['Senate Majority Floor Leader']}</td>    
      <td>{'name-as-written': 'Sen. RUSSELL BLAIR (D) Senate Majority Floor Leader', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5686274509803921, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5686274509803921, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>948782</td>
      <td>{'name-as-written': 'Rep. DWIGHT TAKAMINE (D)', 'name-normalized': 'Takamine, Dwight', 'attributes': ['North Hilo/Hamakua']}</td>
      <td>{'name-as-written': 'Rep. Dwight Takamine (D) North Hilo/Hamakua', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7209302325581395, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.4418604651162791, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>1080013</td>
      <td>{'name-as-written': 'Rep. DAVID IGE (D)', 'name-normalized': 'Ige, David', 'attributes': ['Chairman, Economic Dev. & Hawaiian Affairs Com.']}</td>
      <td>{'name-as-written': 'David Ige, D, Chairman, Economic Dev. & Hawaiian Affairs Com.', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9180327868852459, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.8524590163934426, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-37vmd093 (40 rows)</td>
      <td>1295028</td>
      <td>{'name-as-written': 'Sen. LEHUA FERNANDES SALLING (D)', 'name-normalized': 'Fernandes Salling, Lehua', 'attributes': ['Chairman', 'Senate Transportation Committee']}</td>
      <td>{'name-as-written': 'Sen. LEHUA FERNANDE SALLING (D) Chairman Senate Transportation Committee', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5833333333333334, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5833333333333334, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>108275</td>
      <td>{'name-as-written': 'LESLIE WILCOX', 'name-normalized': 'Wilcox, Leslie', 'attributes': ['ELECTION LIVE']}</td>
      <td>{'name-as-written': 'Leslie Wilcox, Election Live', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8571428571428571, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5357142857142857, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>270904</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Former Congressional Candidate']}</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE Former Congressional Candidate', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>347514</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Keir, Gerry', 'attributes': ['Managing Editor', 'Honolulu Advertiser']}</td>
      <td>{'name-as-written': 'Gerry Keir, Managing Editor, Honolulu Advertiser', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9166666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7916666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>422756</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE', 'name-normalized': 'Radcliffe, John', 'attributes': ['Former Congressional Candidate']}</td>
      <td>{'name-as-written': 'JOHN RADCLIFFE Former Congressional Candidate', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6888888888888889, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>488522</td>
      <td>{'name-as-written': 'GERRY KEIR', 'name-normalized': 'Keir, Gerry', 'attributes': ['Managing Editor', 'Honolulu Advertiser']}</td>
      <td>{'name-as-written': 'Gerry Keir, Managing Editor, Honolulu Advertiser', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9166666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7916666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>784151</td>
      <td>{'name-as-written': 'NINA BERGLUND', 'name-normalized': 'Berglund, Nina', 'attributes': ['Election Live']}</td>
      <td>{'name-as-written': 'NANA BERGLUND Election Live', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5555555555555556, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5555555555555556, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>801635</td>
      <td>{'name-as-written': 'DAN TUTTLE', 'name-normalized': 'Tuttle, Dan', 'attributes': ['Political Analyst']}</td>
      <td>{'name-as-written': 'Dan Tuttle, Political Analyst', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.896551724137931, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6551724137931034, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>830030</td>
      <td>{'name-as-written': 'ANDREW POEPOE', 'name-normalized': 'Poepoe, Andrew', 'attributes': ['Co-Chairman', 'Saiki in '88 Committee']}</td>    
      <td>{'name-as-written': 'ANDREW POEPOE Co-Chairman Saiki in '88 Committee', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7291666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7291666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1068902</td>
      <td>{'name-as-written': 'STAN KOKI (R)', 'name-normalized': 'Koki, Stan', 'attributes': []}</td>
      <td>{'name-as-written': 'STAN KOKI (R)', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1183016</td>
      <td>{'name-as-written': 'CLAYTON HEE (D)', 'name-normalized': 'Hee, Clayton', 'attributes': []}</td>
      <td>{'name-as-written': 'CLAYTON HEE (D)', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-44bnzxh7 (20 rows)</td>
      <td>1417150</td>
      <td>{'name-as-written': 'JERRY BURRIS', 'name-normalized': 'Burris, Jerry', 'attributes': ['Politics Editor', 'Honolulu Advertiser']}</td>     
      <td>{'name-as-written': 'JERRY BURRIS, POLITICS EDITOR, HONOLULU ADVERTISER', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.76, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.76, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>97397</td>
      <td>{'name-as-written': 'LESLIE WILCOX', 'name-normalized': 'Wilcox, Leslie', 'attributes': ['Hawaii Public Television']}</td>
      <td>{'name-as-written': 'Leslie Wilcox, Hawaii Public Television', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9230769230769231, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6666666666666666, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>175876</td>
      <td>{'name-as-written': 'JONATHAN DENNIS', 'name-normalized': 'Dennis, Jonathan', 'attributes': ['Director, The New Zealand Film Archive']}</td>
      <td>{'name-as-written': 'Jonathan Dennis, Director, The New Zealand Film Archive', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9272727272727272, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7272727272727273, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>581381</td>
      <td>{'name-as-written': 'WITARINA HARRIS', 'name-normalized': 'Harris, Witarina', 'attributes': []}</td>
      <td>{'name-as-written': 'WITARINA HARRIS', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>955255</td>
      <td>{'name-as-written': 'WITARINA HARRIS', 'name-normalized': 'Harris, Witarina', 'attributes': []}</td>
      <td>{'name-as-written': 'WITARINA HARRIS', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-48sbchm7 (13 rows)</td>
      <td>1404404</td>
      <td>{'name-as-written': 'JONATHAN DENNIS', 'name-normalized': 'Dennis, Jonathan', 'attributes': ['Director, The New Zealand Film Archive']}</td>
      <td>{'name-as-written': 'Jonathan Dennis, Director, The New Zealand Film Archive', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9272727272727272, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7272727272727273, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>99766</td>
      <td>{'name-as-written': 'Howard Dicus', 'name-normalized': 'Dicus, Howard', 'attributes': ['PBN Friday']}</td>
      <td>{'name-as-written': 'Howard Dicus, PBN Friday', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.5, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>286753</td>
      <td>{'name-as-written': 'Connie Lau', 'name-normalized': 'Lau, Connie', 'attributes': ['CEO', 'American Savings Bank']}</td>
      <td>{'name-as-written': 'Connie Lau, CEO, American Savings Bank', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7368421052631579, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7368421052631579, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>644878</td>
      <td>{'name-as-written': 'Sterling Paulos', 'name-normalized': 'Paulos, Sterling', 'attributes': ['Hotel Director', 'NCL Hawaii']}</td>
      <td>{'name-as-written': 'STERLING PAULOS, Hotel Director, NCL HAWAII', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.8837209302325582, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.6511627906976745, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>954521</td>
      <td>{'name-as-written': 'Susan Todani', 'name-normalized': 'Todani, Susan', 'attributes': ['Director of Investments', 'Kamehameha Schools']}</td>
      <td>{'name-as-written': 'Susan Todani, Director of Investments, Kamehameha Schools', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.7894736842105263, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7894736842105263, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-51vdnj5t (5 rows)</td>
      <td>1032032</td>
      <td>{'name-as-written': 'Rosalind Schurgin', 'name-normalized': 'Schurgin, Rosalind', 'attributes': ['Executive Vice President', 'Festival Companies']}</td>
      <td>{'name-as-written': 'ROSALIND SCHURGIN, EXECUTIVE VICE PRESIDENT, FESTIVAL COMPANIES', 'name-normalized': '', 'attributes': []}</td>       
      <td>{'name-as-written': 0.9523809523809523, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7301587301587301, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-65v6x41w (18 rows)</td>
      <td>250150</td>
      <td>{'name-as-written': 'CHARLES TOGUCHI', 'name-normalized': 'Toguchi, Charles', 'attributes': ['Superintendent', 'Dept. of Education']}</td> 
      <td>{'name-as-written': 'Charles Togechi, Superintendent, Dept. of Education', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.9411764705882353, 'name-normalized': 1.0, 'attributes': 1.0}</td>
      <td>{'name-as-written': 0.7254901960784313, 'name-normalized': 1.0, 'attributes': 1.0}</td>
    </tr>
    <tr>
      <td>cpb-aacip-225-65v6x41w (18 rows)</td>
      <td>1179646</td>
      <td>{'name-as-written': 'Rep. DANIEL KIHANO', 'name-normalized': 'Kihano, Daniel', 'attributes': []}</td>
      <td>{'name-as-written': 'Rep. DANIEL KIHANO', 'name-normalized': '', 'attributes': []}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
      <td>{'name-as-written': 0.0, 'name-normalized': 1.0, 'attributes': 0}</td>
    </tr>
  </tbody>
</table>