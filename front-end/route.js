import {loadTable} from './index.js'

import {loadCountiesTable, showCountyCreateBox} from './county.js'
import {loadPlacesTable, showPlaceCreateBox} from './place.js'
import {loadLotsTable, showLotCreateBox} from './lot.js'
import {loadReservationsTable, showReservationCreateBox} from './reservation.js'
import {loadPaymentsTable, showPaymentCreateBox} from './payment.js'
import { loadReportsTable, loadSelectPlaces } from './reports.js'

//if user is not logged in prompt login
const uname = localStorage.getItem('uname')

if(!uname){
  window.location.href = './sign_in.html'
}
const menus = document.querySelectorAll(".sidebar a")
let page ="home"

menus.forEach(menu=>{
   
   menu.addEventListener("click",()=>{
    menus.forEach(element=>element.removeAttribute('class'))
    
    const content = document.querySelector('.content')
    
    let page_href = menu.getAttribute('href')
    
    page = (!page_href)?page:page_href.replace("#","")

    menu.setAttribute('class','active')
    if( page == 'payments'){
      loadPaymentsTable()
    }else if (page == 'counties') {
     
      loadCountiesTable()
    }else if (page == 'places') {
      
      loadPlacesTable()
      
    }else if (page == 'lots') {
      
      loadLotsTable()
    }else if (page == 'reservations') {
      loadReservationsTable()
    }else if(page == 'reports'){
      loadSelectPlaces()
      
      loadReportsTable()
      
    }else{
      
      window.location.href ='./index.html'
      loadTable()
      
    }
    
    load(content, page+".html")
    if (page == 'payments') {
      setTimeout(()=>{
        document.getElementById('create-payment').addEventListener('click',()=>{
          showPaymentCreateBox()
        })
      },100)
      
      
    }else if (page == 'reservations') {
      setTimeout(()=>{
        document.getElementById('create-reservation').addEventListener('click',()=>{
          showReservationCreateBox()
        })
      } ,100)
      
      
    }
    else if (page == 'lots') {
      setTimeout(()=>{
        document.getElementById('create-lot').addEventListener('click',()=>{
          showLotCreateBox()
        })
      }
      ,100)
     
    }
    else if (page == 'places') {
      setTimeout(()=>{
        document.getElementById('create-place').addEventListener('click',()=>{
          showPlaceCreateBox()
        })
      },100)
      
    }
    else if (page == 'counties') {
      setTimeout(()=>{

        document.getElementById('create-county').addEventListener('click',()=>{
          showCountyCreateBox()
        })
      },100)
      
    }
   })
})

 const load = (target,url)=>{
  fetch(url)
  .then(response =>response.text())
  .then(data=> target.innerHTML = data)
 }