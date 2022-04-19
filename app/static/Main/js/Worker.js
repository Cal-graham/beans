//Chart Worker

onmessage = function(e) {
  console.log(e);
  switch(e.event) {
  case 'init':
    init(e.data); //key for each graph
    break;
    case 'profiling':
    profiling_stage = e.data
    break;
  }
}


//Graph generation//
init = function(data){
  globalThis.graphs = {}
  globalThis.profiling_stage = 0
  globalThis.enable_refresh = 1
  for(const [graph, value] of Object.entries(data)){
      graphs[graph] = new Chart(document.getElementById(graph), {
            type: 'scatter',
            options: chartOptions,
            data: {
              labels: [],
              datasets: [dataset('', 0)]
            }
        });
    var graphs[graph.concat('_maintain')] = 0 
    var graphs[graph.concat('_')] = 0
  }
  
  var requests = $.get('/main/read');
  var tm = requests.done(function(read){
      for (const [key_read, value_read] of Object.entries(read)){
        for(let graph in data){
              if (key_read.includes(graph)){
                add = dataset(graph, graphs[graph.concat('_')]);
                add.data = [{x:r['time'], y:value}]
                graphs[graph].data.datasets[graphs[graph.concat('_')]] = add;
                graphs[graph.concat('_')] += 1;
              }
              graphs[graph.concat('_maintain')] = graphs[graph.concat('_')]
        }
      }
      for (const [key_read, value_read] of Object.entries(read)){
        for(let graph in data){
              if (key_read.includes(graph)){
                add = dataset(graph, graphs[graph.concat('_')] - graphs[graph.concat('_maintain')]);
                add.borderDash = [10,5];
				        add.data = [{x:0,y:0},{x:0,y:0}];
				        add.hidden = true;
                graphs[graph].data.datasets[graphs[graph.concat('_')]] = add;
                graphs[graph.concat('_')] += 1;
              }
        }
      }
    //targetProfiles();
    for(let graph in data){
      graphs[graph].update();
    }
   });
  var source = new EventSource("/main/continuous_read");
	source.onmessage = function(event){
    		console.log(event.data)
		    update_graphs(JSON.parse(event.data))
	}
}

//Graph Updates//
update_graphs = function(r){

                for(let graph in graphs){
                            if (!graph.includes('_')){
                graphs[graph.concat('_')] = 0
                            }}
                for (const [key, value] of Object.entries(r)){
                        for(let graph in graphs){
                            if (!graph.includes('_')){
                        if (key.includes(graph) && enable_refresh == 1){
                                //console.log({{graph}}_)
                                graphs[graph].data.datasets[graphs[graph.concat('_')]].data.push({x:r["time"], y:value})
                                graphs[graph.concat('_')] += 1
                        }
                }}
                        if (key.includes("time")){
                          
                          for(let graph in graphs){
                            if (!graph.includes('_')){
                                graphs[graph].data.labels.push(value)
                                if ( profiling_stage < 3 && graphs[graph].data.labels.length > 400 ){ 
                                        graphs[graph].data.labels.shift();
                                        var graphs[graph.concat('__')] = 0
                                        graphs[graph].data.datasets.forEach((dataset) => {
                                                if (graphs[graph.concat('__')] < graphs[graph.concat('_maintain')]){
                                                        dataset.data.shift();
                                                        graphs[graph.concat('__')] += 1
                                                }
                                        });
                                }
                        }}
                        }
                }

                if (profiling_stage != 0){
                        //profilingStage();
                }
                if (profiling_stage < 4){
                  for(let graph in graphs){
                    if (!graph.includes('_')){
                      setBounds(graphs[graph])
                    }
                  }
                }
    for(let graph in graphs){
      if (!graph.includes('_')){
        graphs[graph].update();
      }
    }
         
//Graph Generation Objects//
             var chartOptions = {
        maintainAspectRatio: false,
        animation: {
                duration: 0 //200
        },
        layout: {
            padding:{
		left: 0,
		right: 0,
		top: 0,
		bottom: -10
	    }
        },
        scales:{
            xAxes: [{
                display: false,
		offset: false,
		grace: '0%'
            }],
        },
        title: {
          display: false
        },
	elements: {
		point : {
			radius: 0
		}
	},
	legend: {
               	display: false,
		position: 'right'
	}
    }

         
    var chartColors = {
        pressure: ['rgb(255, 255, 255)', 'rgb(255, 255, 255)', 'rgb(255, 255, 255)'],
        flow: ['rgb(0, 100, 255)', 'rgb(0, 0, 255)'],
        temperature: ['rgb(255, 0, 100)', 'rgb(255, 100, 0)']
    };

    var color = Chart.helpers.color;
	
    var zeroDataSet = {
	data: [],
        label: "template",
	backgroundColor: chartColors.pressure[0].replace(')', ', 0.10)').replace('rgb', 'rgba'),
        borderColor: chartColors.pressure[0],
        pointBorderColor: chartColors.pressure[0],
        pointBackgroundColor: chartColors.pressure[0],
        fill: true,
        pointRadius: 0,
        outerGlowWidth: 40,
        outerGlowColor: chartColors.pressure[0],
        shadowBlur: 10,
        shadowColor: chartColors.pressure[0]
    };
	 
    dataset = function(type, idx){
	var color = "rgb('255', '255', '255')";
	console.log(graph);
      
	for(let graph in graphs){
  if (!graph.includes('_')){
	if (type.includes(graph)){
		color = chartColors[graph][idx];
        }
    }
  }
	add = $.extend( true, {}, zeroDataSet),
	add.label = graph;
	add.showLine = tr}ue;
	add.backgroundColor = color.replace(')', ', 0.10)').replace('rgb', 'rgba');
	add.borderColor = color
	add.pointBorderColor = color
	add.pointBackgroundColor = color
	add.fill = true
	add.pointRadius = 0
	add.outerGlowWidth = 40
	add.outerGlowColor = color
	add.shadowBlur = 10
	add.shadowColor = color    
	return add
}
         
//Graph Functions//
             clear_graphs = function(min){
	for(let graph in graphs){
                            if (!graph.includes('_')){
	if(graphs[graph].data.datasets[0].data.length > min){
        while (graphs[graph].data.labels.length > min){
		graphs[graph.concat('_')] = 0
                graphs[graph].data.labels.shift();
                graphs[graph].data.datasets.forEach((dataset) => {
                       	if (graphs[graph.concat('_')] <= graphs[graph.concat('_maintain')]){
                        	dataset.data.shift();
				graphs[graph.concat('_')] += 1
                	}
                });
        }
	}
  }}
    }
         
    function setBounds(chart){
	if (chart.data.datasets[0].data.length > 1){
	var min = chart.data.datasets[0].data[0].x
	var max = chart.data.datasets[0].data[chart.data.datasets[0].data.length-1].x
//	chart.data.datasets.forEach((dataset) => {
//		if(dataset.data.length > 1){
//		//console.log(dataset.data)
//		min_ = dataset.data[0].x
//		max_ = dataset.data[dataset.data.length-1].x
        	//console.log(min)
		//console.log(min_)
//		if (min_ < min && min_ != 0){
//                	min = min_
//		}
//		if (max_ > max){
//			max = max_
//		}
//		}
  //      });
	chart.options.scales.xAxes[0].ticks.min = min
	chart.options.scales.xAxes[0].ticks.max = max
//	chart.update();
        }
    }
         
