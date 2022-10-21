export const  showPaymentCreateBox = ()=> {
    Swal.fire({
      title: 'Create payment',
      html:
        '<input id="id" type="hidden">' +
        '<input id="reserve_id" class="swal2-input" placeholder="Reserve ID">' +
        '<input id="reservation_fees" class="swal2-input" placeholder="Reserve Fees" >',
      focusConfirm: false,
      preConfirm: () => {
        
        
        paymentCreate();
        return false
      }
    })
  }
  //reserve_id, reservation_fees

  export const paymentCreate = () => {
    
    const reserve_id = document.getElementById("reserve_id").value;
    const reservation_fees = document.getElementById("reservation_fees").value;
    
    
    if (!(reserve_id && reservation_fees )) {
      Swal.fire("Please fill all the fields")
    }else{

        
          const data ={
              "reserve_id":reserve_id,
              "reservation_fees":reservation_fees,
             
          }
          fetch("http://localhost:5000/api/payments/create", {
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
              loadPaymentsTable();
          })
    
    }

    
}

 export const showPaymentEditBox= (id) =>{
    
   
    fetch("http://localhost:5000/api/payments/"+id)
    .then(response => response.json())
    .then(data=>{
        
        const payment = data.data
        
        Swal.fire({
          title: 'Edit Payment',
          html:
          '<input id="id" type="hidden" value="'+payment['id']+'">'+
          '<input id="reserve_id" class="swal2-input" placeholder="Reserve ID" value="'+payment['reserve_id']+'">' +
          '<input id="reservation_fees" class="swal2-input" placeholder="Reserve Fees" value="'+payment['reservation_fees']+'">',
          focusConfirm: false,
          preConfirm: () => {
            paymentEdit();
          }
        })

    })
 
  }
  
  export const paymentEdit = ()=> {
    const id = document.getElementById("id").value;
    const reserve_id = document.getElementById("reserve_id").value;
    const reservation_fees = document.getElementById("reservation_fees").value;
    
     
    fetch("http://localhost:5000/api/payments/"+id+"/edit",{
        method :'PATCH',
        body:new URLSearchParams({
            "reserve_id":reserve_id,
            "reservation_fees":reservation_fees,
        }),
        headers:new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    })
    .then(response =>response.json())
    .then(data =>{
        Swal.fire(data.message);
        loadPaymentsTable();
    })

  }

  export const paymentDelete = (id)=> {

     
    fetch("http://localhost:5000/api/payments/"+id+"/delete",{
        method:"DELETE",
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    } )
    .then(response =>response.json())
    .then(data=>{
        Swal.fire(data.message);
        loadpaymentsTable();
    })
    
  }
  
  export const loadPaymentsTable = () => {
    fetch("http://localhost:5000/api/payments")
    .then(response=>response.json())
    .then(data=>{
        
        var trHTML = ''; 
        
        for (let object of data.data) {
           
          trHTML += '<tr>'; 
          trHTML += '<td>'+object['id']+'</td>';
        
          trHTML += '<td>'+object['reserve_id']+'</td>';
          trHTML += '<td>'+object['reservation_fees']+'</td>';
          trHTML += '<td><button type="button" class="btn btn-outline-secondary edit-action" data-id="'+ object['id']+'">Edit</button>';
          trHTML += '<button type="button" class="btn btn-outline-danger delete-action"  data-id="'+ object['id']+'">Del</button></td>';
          trHTML += "</tr>";
          
        }
        document.getElementById("mytable").innerHTML = trHTML;
      
        const edit_buttons = document.querySelectorAll('.edit-action')
        
        edit_buttons.forEach(edit_button =>{
          edit_button.addEventListener('click',()=>{
            showPaymentEditBox(edit_button.getAttribute('data-id'))
          })
        })
      
        const delete_buttons = document.querySelectorAll('.delete-action')
        
        delete_buttons.forEach(delete_button =>{
          delete_button.addEventListener('click',()=>{
            paymentDelete(delete_button.getAttribute('data-id'))
          })
        })

    })
   
  }
