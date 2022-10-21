  export const loadSelectPlaces = ()=>{
    
    fetch("http://localhost:5000/api/places")
    .then(response => response.json())
    .then(data=>{
        const place_array = data.data
        let new_option_elements=`<option value=${null}>Select Place</option>`
        place_array.forEach(place => {
            new_option_elements +=`<option value='${place.id}'> ${place.place_name} </option>`
            
        });
            
        document.getElementById("places").innerHTML += new_option_elements
        

    })
  }
  export const loadReportsTable = () => {
    let query_string ="?"
    let id=null
    setTimeout(() => {
        document.getElementById('places').addEventListener('change',(event)=>{
            // console.log(event.target);
         id = event.target.value
         dynamicReport(id,document.getElementById('start_date').value,document.getElementById('stop_date').value)
         let start_date = null

         document.getElementById('start_date').addEventListener('change',(event)=>{

            start_date = event.target.value
            dynamicReport(id,start_date,document.getElementById('stop_date').value)
            
        })
        
        let stop_date = null
        document.getElementById('stop_date').addEventListener('change',(event)=>{

            stop_date = event.target.value
            dynamicReport(id,document.getElementById('start_date').value,stop_date)
            
        })
           

        })
        }, 200);
    
  }


  const dynamicReport = (id,start_date,stop_date)=>{
    let query_string ="?"
    if(start_date){
        query_string += "start_date="+start_date+"&"
    }
    if(stop_date){
        query_string += "stop_date="+stop_date

    }
    fetch("http://localhost:5000/api/places/"+id+"/reservations"+query_string)
    .then(response=>response.json())
    .then(data=>{
        
        var trHTML = ''; 
        
        for (let object of data.data) {
        
        trHTML += '<tr>'; 
        trHTML += '<td>'+object['id']+'</td>';
        trHTML += '<td>'+object['lot_id']+'</td>';
        trHTML += '<td>'+object['vehicle_category']+'</td>';
        trHTML += '<td>'+object['vehicle_plate']+'</td>';
        trHTML += '<td>'+object['reserve_date']+'</td>';
        trHTML += '<td>'+object['start_time']+'</td>';
        trHTML += '<td>'+object['end_time']+'</td>';
        trHTML += '<td>'+object['user_id']+'</td>';
        trHTML += "</tr>";
        
        }
        document.getElementById("mytable").innerHTML = trHTML;
    
        
    })

    
  }


 