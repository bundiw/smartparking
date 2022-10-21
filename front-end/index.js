export const  showUserCreateBox = ()=> {
    Swal.fire({
      title: 'Create user',
      html:
        '<input id="id" type="hidden">' +
        '<input id="full_name" class="swal2-input" placeholder="Full Name">' +
        '<input id="phone_number" class="swal2-input" placeholder="Phone Number" >' +
        '<input id="email" class="swal2-input" placeholder="Email" >' +
        '<input id="password" class="swal2-input" placeholder="Password" >'+
        '<input id="cpassword" class="swal2-input" placeholder="Confirm Password">',
      focusConfirm: false,
      preConfirm: () => {
        
        
        userCreate();
        return false
      }
    })
  }
  
  document.getElementById('create-data').addEventListener('click',()=>{
    showUserCreateBox()
  })      
  
  export const userCreate = () => {
    
    const full_name = document.getElementById("full_name").value;
    const phone_number = document.getElementById("phone_number").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const cpassword = document.getElementById("cpassword").value;
    if (!(full_name && phone_number && email && password)) {
      Swal.fire("Please fill all the fields")
    }else{

      if (password == cpassword) {
         
        
          const data ={
              "full_name":full_name,
              "phone_number":phone_number,
              "email":email,
              "password":password
          }
          fetch("http://localhost:5000/api/users/create", {
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
              loadTable();
          })
      }else{
          Swal.fire("Confirm Password must match Password value")
  
      }
    }

    
}

 export const showUserEditBox= (id) =>{
    
   
    fetch("http://localhost:5000/api/users/"+id)
    .then(response => response.json())
    .then(data=>{
        
        const user = data.data
        
        Swal.fire({
          title: 'Edit User',
          html:
            '<input id="id" type="hidden" value='+user['id']+'>' +
            '<input id="full_name" class="swal2-input" placeholder="Full Name" value="'+user['full_name']+'">' +
            '<input id="phone_number" class="swal2-input" placeholder="Phone Number" value="'+user['phone_number']+'">' +
            '<input id="email" class="swal2-input" placeholder="Email" value="'+user['email']+'">' +
            '<input disabled id="password" class="swal2-input" placeholder="Password" value="'+user['password']+'">',
          focusConfirm: false,
          preConfirm: () => {
            userEdit();
          }
        })

    })
 
  }
  
  export const userEdit = ()=> {
    const id = document.getElementById("id").value;
    const full_name = document.getElementById("full_name").value;
    const phone_number = document.getElementById("phone_number").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
     
    fetch("http://localhost:5000/api/users/"+id+"/edit",{
        method :'PATCH',
        body:new URLSearchParams({
            "full_name":full_name,
            "phone_number":phone_number,
            "email":email,
            "password":password
        }),
        headers:new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    })
    .then(response =>response.json())
    .then(data =>{
        Swal.fire(data.message);
        loadTable();
    })

  }

  export const userDelete = (id)=> {

     
    fetch("http://localhost:5000/api/users/"+id+"/delete",{
        method:"DELETE",
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    } )
    .then(response =>response.json())
    .then(data=>{
        Swal.fire(data.message);
        loadTable();
    })
    
  }
  
  export const loadTable = () => {
    fetch("http://localhost:5000/api/users")
    .then(response=>response.json())
    .then(data=>{
        
        var trHTML = ''; 
        
        for (let object of data.data) {
           
          trHTML += '<tr>'; 
          trHTML += '<td>'+object['id']+'</td>';
        
          trHTML += '<td>'+object['full_name']+'</td>';
          trHTML += '<td>'+object['phone_number']+'</td>';
          trHTML += '<td>'+object['email']+'</td>';
          trHTML += '<td><button type="button" class="btn btn-outline-secondary edit-action" data-id="'+ object['id']+'">Edit</button>';
          trHTML += '<button type="button" class="btn btn-outline-danger delete-action"  data-id="'+ object['id']+'">Del</button></td>';
          trHTML += "</tr>";
          
        }
        document.getElementById("mytable").innerHTML = trHTML;
      
        const edit_buttons = document.querySelectorAll('.edit-action')
        
        edit_buttons.forEach(edit_button =>{
          edit_button.addEventListener('click',()=>{
            showUserEditBox(edit_button.getAttribute('data-id'))
          })
        })
      
        const delete_buttons = document.querySelectorAll('.delete-action')
        
        delete_buttons.forEach(delete_button =>{
          delete_button.addEventListener('click',()=>{
            userDelete(delete_button.getAttribute('data-id'))
          })
        })

    })
   
  }


loadTable();  

