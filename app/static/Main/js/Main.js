
    var lineData = {
      labels: ['1'],
      datasets: [{
        data: [1],
        label: "grp1"
      }, {
        data: [1],
        label: "grp2"
      }, {
        data: [1],
        label: "grp3"
      },{
        data: [1],
        label: "blr1"
      },{
        data: [1],
        label: "blr2"
      }, {
        data: [1],
        label: "blr3"
      }]
    };

    var lineChart = new Chart(document.getElementById("lineChart"), {
      type: 'line',
      data: lineData,
      options: {
        title: {
          display: true,
          text: 'Temp Profile'
        }
      }
    });

    var polarData = {
      labels: ["grp1", "grp2", "grp3", "blr1", "blr2", "blr3"],
      datasets: [{
        data: [1, 1, 1, 1, 1, 1],
        backgroundColor: [
          "rgba(255, 0, 100, 0.6)",
          "rgba(255, 0, 50, 0.6)",
          "rgba(255, 0, 0, 0.6)",
          "rgba(0, 255,200, 0.6)",
          "rgba(200, 0, 200, 0.6)",
          "rgba(0, 255, 0, 0.6)"
        ]
      }]
    };

    var polarChartOptions = {
      startAngle: -Math.PI / 4,
      animation: {
        animateRotate: true
      }
      plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Polar Area Chart'
      }
    }
   };

    var polarAreaChart = new Chart(document.getElementById("polarChart");, {
      type: 'polarArea',
      data: polarData,
      options: polarChartOptions
    });

    var refresh = function(){
        var requests = $.get('/main/read');
        var tm = requests.done(function(r){
		console.log(r)
		console.log(polarAreaChart.data.datasets)
                polarAreaChart.data.datasets[0].data = [r[1], r[2], r[3], r[4], r[5], r[6]];
                polarAreaChart.update();

        });
    }

    var refresh = function(){
        var requests = $.get('/main/read');
        var tm = requests.done(function(r){
		console.log(r)
		console.log(lineChart.data.datasets)
		console.log(lineChart.data.labels)
        console.log(polarAreaChart.data.datasets)

                polarAreaChart.data.datasets[0].data = [r[1], r[2], r[3], r[4], r[5], r[6]];
                polarAreaChart.update();

		        var labels = lineChart.data.labels,
                    shift0 = labels.data.length > 80;

                console.log(labels)

		        var gpHd1 = lineChart.data.datasets[0],
                    shift1 = gpHd1.data.length > 80;
                var gpHd2 = lineChart.data.datasets[1],
                    shift2 = gpHd2.data.length > 80;
                var gpHd3 = lineChart.data.datasets[2],
                    shift3 = gpHd3.data.length > 80;

                console.log(gpHd1)

                var blr1 = lineChart.data.datasets[3],
                    shift4 = blr1.data.length > 80;
                var blr2 = lineChart.data.datasets[4],
                    shift5 = blr2.data.length > 80;
                var blr3 = lineChart.data.datasets[5],
                    shift6 = blr3.data.length > 80;

                // add the point
                lineChart.data.labels = labels;
                lineChart.data.datasets[0] = shift1;
                lineChart.data.datasets[1] = shift2;
                lineChart.data.datasets[2] = shift3;
                lineChart.data.datasets[3] = shift4;
                lineChart.data.datasets[4] = shift5;
                lineChart.data.datasets[5] = shift6;

                lineChart.update();
        });
    }

   setInterval(refresh, 1000);
