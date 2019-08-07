// ライブラリのロード
// name:visualization(可視化),version:バージョン(1),packages:パッケージ(corechart)
google.load('visualization', '1', {'packages':['corechart']});     
google.setOnLoadCallback(drawChart);

// グラフの描画   
function drawChart() {         

    // 配列からデータの生成
    var array_data = [['token', 'freq']]
    this.list.forEach( function(value){
        array_data.push(value)
    })
    var data = google.visualization.arrayToDataTable(array_data);

    // オプションの設定
    var options = {
        title: '単語の出現頻度ベクトル',
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
