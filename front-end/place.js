export const showPlaceCreateBox =() =>{
    Swal.fire({
      title: 'Create Place',
      html:
        '<input id="id" type="hidden">' +
        '<input id="place_name" class="swal2-input" placeholder="place Name" >'+
        '<input id="county_id" class="swal2-input" placeholder="County Id" >',
      focusConfirm: false,
      preConfirm: () => {
        
        placeCreate();
        return false
      }
    })
  }
  
export const placeCreate = ()=> {
    
    const place_name = document.getElementById("place_name").value;
    const county_id = document.getElementById("county_id").value;
    
    if (place_name && county_id) {
       
      
        const data ={
            "place_name":place_name,
            "county_id":county_id,
            
        }
        fetch("http://localhost:5000/api/places/create", {
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
            loadPlacesTable();
        })
    }else{
        Swal.fire("Please fill the fields")

    }

    
}

  export const showplaceEditBox = (id) =>{
    
    fetch("http://localhost:5000/api/places/"+id)
    .then(response => response.json())
    .then(data=>{
        
        const place = data.data
        
        Swal.fire({
          title: 'Edit Place',
          html:
            '<input id="id" type="hidden" value='+place['id']+'>' +
            '<input id="place_name" class="swal2-input" placeholder="place Name" value="'+place['place_name']+'">'+
            '<input id="county_id" class="swal2-input" placeholder="County ID" value="'+place['county_id']+'">',
        
          focusConfirm: false,
          preConfirm: () => {
            placeEdit();
          }
        })

    })
 
  }
  
  export const placeEdit = ()=> {
    const id = document.getElementById("id").value;
    
    const place_name = document.getElementById("place_name").value;
    const county_id = document.getElementById("county_id").value;

    fetch("http://localhost:5000/api/places/"+id+"/edit",{
        method :'PATCH',
        body:new URLSearchParams({
            "place_name":place_name,
            "county_id":county_id,
            
        }),
        headers:new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    })
    .then(response =>response.json())
    .then(data =>{
        Swal.fire(data.message);
        loadPlacesTable();
    })

  }

  export const placeDelete = (id) =>{

     
    fetch("http://localhost:5000/api/places/"+id+"/delete",{
        method:"DELETE",
        headers: new Headers({
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Access-Control-Allow-Origin": "*" 
        })
    } )
    .then(response =>response.json())
    .then(data=>{
        Swal.fire(data.message);
        loadPlacesTable();
    })
    
  }
  export const loadPlacesTable = ()=> {
    fetch("http://localhost:5000/api/places")
    .then(response=>response.json())
    .then(data=>{
        
        var trHTML = ''; 
        
        for (let object of data.data) {
           
          trHTML += '<tr>'; 
          trHTML += '<td>'+object['id']+'</td>';
        
          trHTML += '<td>'+object['place_name']+'</td>'; 
          trHTML += '<td>'+object['county_id']+'</td>'; 
          trHTML += '<td><button type="button" class="btn btn-outline-secondary edit-action" data-id="'+ object['id']+'">Edit</button>';
          trHTML += '<button type="button" class="btn btn-outline-danger delete-action"  data-id="'+ object['id']+'">Del</button></td>';
          trHTML += "</tr>";
          
        }
        document.getElementById("mytable").innerHTML = trHTML;
      
        const edit_buttons = document.querySelectorAll('.edit-action')
        
        edit_buttons.forEach(edit_button =>{
          edit_button.addEventListener('click',()=>{
            showplaceEditBox(edit_button.getAttribute('data-id'))
          })
        })
      
        const delete_buttons = document.querySelectorAll('.delete-action')
        
        delete_buttons.forEach(delete_button =>{
          delete_button.addEventListener('click',()=>{
            placeDelete(delete_button.getAttribute('data-id'))
          })
        })
     

    })
   
  }
  