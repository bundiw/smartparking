export const  showLotCreateBox = ()=> {
    Swal.fire({
      title: 'Create Lot',
      html:
        '<input id="id" type="hidden">' +
        '<input id="place_id" class="swal2-input" placeholder="Place ID">' +
        '<input id="lot_number" class="swal2-input" placeholder="Lot Number" >' +
        '<input id="lot_price" class="swal2-input" placeholder="Lot Price" >',
      focusConfirm: false,
      preConfirm: () => {
        
        
        lotCreate();
        return false
      }
    })
  }
  
//   place_id,lot_number,lot_price
  export const lotCreate = () => {
    
    const place_id = document.getElementById("place_id").value;
    // const phone_number = document.getElementById("phone_number").value;
    const lot_number = document.getElementById("lot_number").value;
    const lot_price = document.getElementById("lot_price").value;
    
    if (!(place_id && lot_number && lot_price)) {
      Swal.fire("Please fill all the fields")
    }else{

        
          const data ={
              "place_id":place_id,
              "lot_number":lot_number,
              "lot_price":lot_price,
             
          }
          fetch("http://localhost:5000/api/lots/create", {
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
              loadLotsTable();
          })
    
    }

    
}

 export const showLotEditBox= (id) =>{
    
   
    fetch("http://localhost:5000/api/lots/"+id)
    .then(response => response.json())
    .then(data=>{
        
        const lot = data.data
        
        Swal.fire({
          title: 'Edit Lot',
          html:
          '<input id="id" type="hidden" value="'+lot['place_id']+'">' +
          '<input id="place_id" class="swal2-input" placeholder="Place ID" value="'+lot['place_id']+'">'+
          '<input id="current_use" class="swal2-input" placeholder="Current Use" disabled="true" value="'+lot['current_use']+'">' +
          '<input id="lot_price" class="swal2-input" placeholder="Lot Price" value="'+lot['lot_price']+'">',
          focusConfirm: false,
          preConfirm: () => {
            lotEdit();
          }
        })

    })
 
  }
  
  export const lotEdit = ()=> {
    const id = document.getElementById("id").value;
    const place_id = document.getElementById("place_id").value;
    const current_use = document.getElementById("current_use").value;
    const lot_price = document.getElementById("lot_price").value;
    
    fetch("http://localhost:5000/api/lots/"+id+"/edit",{
        method :'PATCH',
        body:new URLSearchParams({
            "place_id":place_id,
            "lot_price":lot_price,
            "current_use":current_use
        }),
        headers:new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    })
    .then(response =>response.json())
    .then(data =>{
        Swal.fire(data.message);
        loadLotsTable();
    })

  }

  export const lotDelete = (id)=> {

     
    fetch("http://localhost:5000/api/lots/"+id+"/delete",{
        method:"DELETE",
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    } )
    .then(response =>response.json())
    .then(data=>{
        Swal.fire(data.message);
        loadLotsTable();
    })
    
  }
  
  export const loadLotsTable = () => {
    fetch("http://localhost:5000/api/lots")
    .then(response=>response.json())
    .then(data=>{
        
        var trHTML = ''; 
        
        for (let object of data.data) {
           
          trHTML += '<tr>'; 
          trHTML += '<td>'+object['id']+'</td>';
        
          trHTML += '<td>'+object['lot_number']+'</td>';
          trHTML += '<td>'+object['place_id']+'</td>';
          trHTML += '<td>'+object['lot_price']+'</td>';
          trHTML += '<td>'+object['current_use']+'</td>';
          trHTML += '<td><button type="button" class="btn btn-outline-secondary edit-action" data-id="'+ object['id']+'">Edit</button>';
          trHTML += '<button type="button" class="btn btn-outline-danger delete-action"  data-id="'+ object['id']+'">Del</button></td>';
          trHTML += "</tr>";
          
        }
        document.getElementById("mytable").innerHTML = trHTML;
      
        const edit_buttons = document.querySelectorAll('.edit-action')
        
        edit_buttons.forEach(edit_button =>{
          edit_button.addEventListener('click',()=>{
            showLotEditBox(edit_button.getAttribute('data-id'))
          })
        })
      
        const delete_buttons = document.querySelectorAll('.delete-action')
        
        delete_buttons.forEach(delete_button =>{
          delete_button.addEventListener('click',()=>{
            lotDelete(delete_button.getAttribute('data-id'))
          })
        })

    })
   
  }
