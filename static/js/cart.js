
var updateBtns= document.getElementsByClassName('update-cart')



for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click' , function(){
        var productId=this.dataset.product
        var action=this.dataset.action
        var p_quantity =document.getElementById('quantity').value

        console.log('productId:',productId ,'action:',action,'quantity:', p_quantity)
        

        console.log('USER:',user)
        if(user === 'AnonymousUser'){
            console.log('User is not authenticated')
        }
        else{
            updateUserOrder(productId, action, p_quantity)
        }
    })
}

function updateUserOrder(productId, action,p_quantity){
    console.log('User is authenticated, sending data...')
    
    var url='/update_item/'
    
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action,'p_quantity':p_quantity})
    })
    
    
    .then((response)=>{
        return response.json();
    })
    
    
    .then((data)=>{
        console.log('Data:', data)
        location.reload()
    })

}



