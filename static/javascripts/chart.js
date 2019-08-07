// ライブラリのロード
// name:visualization(可視化),version:バージョン(1),packages:パッケージ(corechart)
google.load('visualization', '1', {'packages':['corechart']});     
google.setOnLoadCallback(drawChart);

// グラフの描画   
function drawChart() {         

    // 配列からデータの生成
    var data = google.visualization.arrayToDataTable([
        ['年度', '所得税', '法人税','消費税'],
        ['H19年度',  16.08 , 14.74 , 10.27],
        ['H20年度',  14.99 , 10.01 ,  9.97],            
        ['H21年度',  12.91 ,  6.36 ,  9.81],
        ['H22年度',  12.98 ,  8.97 , 10.03], 
        ['H23年度',  13.48 ,  9.35 , 10.19],
        ['H24年度',  13.99 ,  9.76 , 10.35],
        ['H25年度',  15.53 , 10.49 , 10.83]  
    ]);

    // オプションの設定
    var options = {
        title: '租税の年間推移 ( 単位：兆円 )',
    };        

    /* 積み上げ棒グラフ
    // オプションの設定
    var options = {
        title: '租税の年間推移 ( 単位：兆円 )',
        isStacked: true
    };    
    */
                    
    // 指定されたIDの要素に棒グラフを作成
    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));

    /* 横グラフ
    // 指定されたIDの要素に棒グラフを作成
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));    
    */ 
    // グラフの描画
    chart.draw(data, options);
}
