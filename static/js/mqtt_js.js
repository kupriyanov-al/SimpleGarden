console.log("TEST");
var mqtt_server = "test.mosquitto.org";
var mqtt_port = "1883";
var mqtt_destname = "";
let temperatura = 0;
let humidity = 0;
let datastamp="";

var btnQuery = document.getElementById('btnQuery');
var myCheckbox = document.getElementById('myCheckbox');
myCheckbox.checked = true;


// выставляем дату текущую и текущую-1
var date = new Date();
var datend = date.toISOString().substring(0, 10);
date.setDate(date.getDate() - 1);
var datest = date.toISOString().substring(0, 10);

// устанавливаем значение даты
document.getElementById('datest').value = datest;
document.getElementById('datend').value = datend;


//client = new Paho.MQTT.Client("mqtt.hostname.com", Number(8080), "", "clientId");
client = new Paho.MQTT.Client("test.mosquitto.org" ,Number(8081),"","clientId")
//client = new Paho.MQTT.Client("test.mosquitto.org" ,Number(1883),"","clientId")

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});


function fetchMonitoring() {
  fetch('http://127.0.0.1:8000/home/db/')
    .then(response => response.json())
    .then(data => showdata(data));
}

if (myCheckbox.checked) {
  fetchMonitoring();
}

myCheckbox.addEventListener('change', function(){
  if (myCheckbox.checked) {
    fetchMonitoring(); 
    btnQuery.setAttribute('disabled', true);
    document.getElementById('datest').setAttribute('disabled', true);
    document.getElementById('datend').setAttribute('disabled', true);
    
  } else {
    btnQuery.removeAttribute('disabled');
    document.getElementById('datend').removeAttribute('disabled');
    document.getElementById('datest').removeAttribute('disabled');
  }
})

// const url = new URL('http://myapi.com/orders');
// url.searchParams.set('order_id', '1');
// fetch(url);

function formatdate(str){
  
  const [year, month, day] = str.split('-');
  var rez = `${day}.${month}.${year}`;
  return rez
}

//вешаем на него событие
btnQuery.onclick = function () {
  var datest = formatdate(document.getElementById('datest').value) ;
  var datend = formatdate(document.getElementById('datend').value) ;
  console.log(datest);
  // var datend = document.getElementById('datend'); 
  //производим  действия
  fetch('http://127.0.0.1:8000/home/'+datest+'/'+datend+'')
  // fetch('http://127.0.0.1:8000/home/01.11.2023/09.12.2023')
    .then(response => response.json())
    .then(data => showdata(data));
}



function showdata(data) {
  for (let r of data) {
    console.log(r)
    myChart.data.labels.push(r.datastamp);
    myChart.data.datasets[0].data.push(r.temperatura);
    myChart.data.datasets[1].data.push(r.humidity);
    myChart.data.datasets[2].data.push(r.releState);
    myChart.data.datasets[3].data.push(r.coolState);
    

    if (myChart.data.datasets[0].data.length > 50) {
      myChart.data.labels.shift();
      myChart.data.datasets[0].data.shift();
    }

    myChart.update();
  }
  
}


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");

  client.subscribe("rasp");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
      console.log("onConnectionLost:"+responseObject.errorMessage);
    }
  }

// called when a message arrives
function onMessageArrived(message) {
    //console.log("onMessageArrived:"+message.payloadString);
    var result = message.destinationName + " : " + message.payloadString + "";
    mes = JSON.parse(message.payloadString);
    //console.log(mes)
    
    temperatura = mes['temperatura'];
    humidity = mes['humidity'];
    coolState = mes['CoolState'];
    releState = mes['ReleState'];

    datastamp = mes['datastamp'];


    coolState=(coolState==true)?'ON':'OFF';
    releState=(releState==true)?'ON':'OFF';

    // document.querySelector(".submsg").innerHTML = temperatura; 
    document.getElementById("temperature").innerHTML = temperatura; 
    document.getElementById("humidity").innerHTML = humidity;
    document.getElementById("coolState").innerHTML = coolState;
    document.getElementById("releState").innerHTML = releState;
    document.getElementById("datastamp").innerHTML = datastamp;
    
    let data=[];
    data.push(mes) 
// Тренды
    console.log(data)

    if (myCheckbox.checked) {
      showdata(data)
    }
    
  
    // myChart.data.labels.push(datastamp);
    // myChart.data.datasets[0].data.push(temperatura);
    
    // console.log(myChart.data.datasets[0].data.length) 
    // if (myChart.data.datasets[0].data.length > 50) {
    //   myChart.data.labels.shift();
    //   myChart.data.datasets[0].data.shift();
    // }
    // myChart.update();
}

var canvas = document.getElementById('myChart');
var myChart = new Chart(canvas, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: "Температура",
      borderColor: "#3e95cd",
      backgroundColor: "#7bb6dd",
      fill: false,
      tension: 0.3,
      data: [],
      stepped: true,
      
      
      yAxisID: 'A',
      
    }, {
      yAxisID: 'B',
      data: [],
      stepped: true,
      label: "Влажность",
      borderColor: "#3cba9f",
      backgroundColor: "#71d1bd",
      fill: false,
      //       // maxTicksLimit: 10,
    },
      {
        yAxisID: 'C',
        data: [],
        stepped: true,
        label: "Освещение",
        borderColor: "#fc1d42",
        backgroundColor: "#71d1bd",
        fill: false,
        
        //       // maxTicksLimit: 10,

      },
      {
        yAxisID: 'D',
        data: [],
        stepped: true,
        label: "Вентилятор",
        borderColor: "#0eec51",
        backgroundColor: "#71d1bd",
        fill: false,
        //       // maxTicksLimit: 10,

      },
  ]
  },
  options: {
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Time'
        },
        ticks: {
          autoSkip: true,
          maxTicksLimit: 20,
          // max:3,
          // min:3,

          
        }
      }],
      yAxes: [{
        
        scaleLabel: {
                  display: true,
                  labelString: 'Temperature'
                },
        id: 'A',
        type: 'linear',
        position: 'left',
        
        ticks: {
          max: 50,
          min: 0
        }
      },
      {

        id: 'B',
        scaleLabel: {
          display: true,
          labelString: 'Влажность'
        },
        type: 'linear',
        position: 'right',
        ticks: {
          max: 100,
          min: 0
        } 
      },
      {
        id: 'C',
        type: 'linear',
        display: false,
        // position: 'left',
        ticks: {
          max: 2,
          min: 0
        } 
      },
      {
        id: 'D',
        type: 'linear',
        display: false,
        ticks: {
          max: 2,
          min: 0
        },
        stepped: true,
      }
    ]
    }
  }
});

// var ctx = document.getElementById('myChart').getContext('2d');
// var myChart = new Chart(ctx, {
//   type: 'line',
//   data: {
//     labels: [],
//     datasets: [{
//       data: [],
//       // yAxisID: 'y1',
//       label: "Температура",
//       borderColor: "#3e95cd",
//       backgroundColor: "#7bb6dd",
//       fill: false,
//       min: 0,
//       max: 50, 
       
//     },
//     {
//       data: [],
//       // yAxisID: 'y2',
//       label: "Влажность",
//       borderColor: "#3cba9f",
//       backgroundColor: "#71d1bd",
//       fill: false,
//       // maxTicksLimit: 10,
//       min: 0,
//       max: 100,
     
//       // 
//     }
//     ]
//   },



//   options: {
//     responsive: true,
//     title: {
//       display: true,
//       text: 'Тренды'
//     },
//     scales: {
//       xAxes: [{
//         display: true,
//         scaleLabel: {
//           display: true,
//           labelString: 'Time'
//         },
//         ticks: {
//           autoSkip: true,
//           // maxTicksLimit: 3,
//           // max:3,
//           // min:3,

          
//         }
//       }],
//       yAxes: [{
//         display: true,
        
//         scaleLabel: {
//           display: true,
//           labelString: 'Temperature'
//         },
//         ticks: {
//           beginAtZero: true,
//           stepSize: 25, 
//         },
        

        
//       }]
//     }
//   }

// });