export const  showReservationCreateBox = ()=> {
    Swal.fire({
      title: 'Create reservation',
      html:
        '<input id="id" type="hidden">' +
        '<input id="lot_id" class="swal2-input" placeholder="Lot ID">' +
        '<input id="vehicle_category" class="swal2-input" placeholder="Vehicle Category">' +
        '<input id="vehicle_plate" class="swal2-input" placeholder="Vehicle Plate">' +
        '<input id="reserve_date" class="swal2-input" placeholder="Reserve Date">' +
        '<input id="start_time" class="swal2-input" placeholder="Start Time">' +
        '<input id="end_time" class="swal2-input" placeholder="End Time" >' +
        '<input id="user_id" class="swal2-input" placeholder="User ID" >',
      focusConfirm: false,
      preConfirm: () => {
        
        
        reservationCreate();
        return false
      }
    })
  }
  
  export const reservationCreate = () => {
    
    const lot_id = document.getElementById("lot_id").value;
    const vehicle_category = document.getElementById("vehicle_category").value;
    const vehicle_plate = document.getElementById("vehicle_plate").value;
    const reserve_date = document.getElementById("reserve_date").value;
    const start_time = document.getElementById("start_time").value;
    const end_time = document.getElementById("end_time").value;
    const user_id = document.getElementById("user_id").value;
    
    if (!(lot_id && vehicle_category && vehicle_plate && reserve_date && start_time && end_time && user_id)) {
      Swal.fire("Please fill all the fields")
    }else{

        
          const data ={
              "lot_id":lot_id,
              "vehicle_category":vehicle_category,
              "vehicle_plate":vehicle_plate,
              "reserve_date":reserve_date,
              "start_time":start_time,
              "end_time":end_time,
              "user_id":user_id,
          }
          fetch("http://localhost:5000/api/reservations/create", {
              method: 'POST',
              body: new URLSearchParams(data),
              headers: new Headers({
                  'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                  "Access-Control-Allow-Origin": "*" 
              })
          })
          .then((response)=>response.json())
          .then(data=>{
             
              Swal.fire(data.message);
              loadReservationsTable();
          })
    
    }

    
}

 export const showReservationEditBox= (id) =>{
    
   
    fetch("http://localhost:5000/api/reservations/"+id)
    .then(response => response.json())
    .then(data=>{
        
        const reservation = data.data
        
        Swal.fire({
          title: 'Edit reservation',
          html:
            '<input id="id" type="hidden" value="'+reservation['id']+'">' +
            '<input id="lot_id" class="swal2-input" placeholder="Lot ID" value="'+reservation['lot_id']+'">' +
            '<input id="vehicle_category" class="swal2-input" placeholder="Vehicle Category" value="'+reservation['vehicle_category']+'">' +
            '<input id="vehicle_plate" class="swal2-input" placeholder="Vehicle Plate" value="'+reservation['vehicle_plate']+'">' +
            '<input id="reserve_date" class="swal2-input" placeholder="Reserve Date" value="'+reservation['reserve_date']+'">' +
            '<input id="start_time" class="swal2-input" placeholder="Start Time" value="'+reservation['start_time']+'">' +
            '<input id="end_time" class="swal2-input" placeholder="End Time" value="'+reservation['end_time']+'">' +
            '<input id="user_id" class="swal2-input" placeholder="User ID" value="'+reservation['user_id']+'">',
          focusConfirm: false,
          preConfirm: () => {
            reservationEdit();
          }
        })

    })
 
  }
  
  export const reservationEdit = ()=> {
    const id = document.getElementById("id").value;
    const lot_id = document.getElementById("lot_id").value;
    const vehicle_category = document.getElementById("vehicle_category").value;
    const vehicle_plate = document.getElementById("vehicle_plate").value;
    const reserve_date = document.getElementById("reserve_date").value;
    const start_time = document.getElementById("start_time").value;
    const end_time = document.getElementById("end_time").value;
    const user_id = document.getElementById("user_id").value;
   
     
    fetch("http://localhost:5000/api/reservations/"+id+"/edit",{
        method :'PATCH',
        body:new URLSearchParams({
            "lot_id":lot_id,
            "vehicle_category":vehicle_category,
            "vehicle_plate":vehicle_plate,
            "reserve_date":reserve_date,
            "start_time":start_time,
            "end_time":end_time,
            "user_id":user_id
        }),
        headers:new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    })
    .then(response =>response.json())
    .then(data =>{
        Swal.fire(data.message);
        loadReservationsTable();
    })

  }

  export const reservationDelete = (id)=> {

     
    fetch("http://localhost:5000/api/reservations/"+id+"/delete",{
        method:"DELETE",
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    } )
    .then(response =>response.json())
    .then(data=>{
        Swal.fire(data.message);
        loadReservationsTable();
    })
    
  }
  
//  lot_id,vehicle_category,vehicle_plate,reserve_date,
// start_time,end_time,user_id
  export const loadReservationsTable = () => {
    fetch("http://localhost:5000/api/reservations")
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
          trHTML += '<td><button type="button" class="btn btn-outline-secondary edit-action" data-id="'+ object['id']+'">Edit</button>';
          trHTML += '<button type="button" class="btn btn-outline-danger delete-action"  data-id="'+ object['id']+'">Del</button></td>';
          trHTML += "</tr>";
          
        }
        document.getElementById("mytable").innerHTML = trHTML;
      
        const edit_buttons = document.querySelectorAll('.edit-action')
        
        edit_buttons.forEach(edit_button =>{
          edit_button.addEventListener('click',()=>{
            showReservationEditBox(edit_button.getAttribute('data-id'))
          })
        })
      
        const delete_buttons = document.querySelectorAll('.delete-action')
        
        delete_buttons.forEach(delete_button =>{
          delete_button.addEventListener('click',()=>{
            reservationDelete(delete_button.getAttribute('data-id'))
          })
        })

    })
   
  }

 