console.log("Working");

const cartbtn = document.getElementsByClassName("update-cart");

for(let i = 0 ;i < cartbtn.length;i++){
    cartbtn[i].addEventListener('click',function(){
        product_id = this.dataset.product_id ;
        action = this.dataset.action;
        console.log("Button is clicked");
        if(customer != "AnonymousUser")
        {
            AddCartFunction(product_id,action)
        }
        else{
            // console.log("You are not login ! First Login Then You Add")
            alert("You are not login ! First Login Then You Add")
        }
    })
}

function AddCartFunction(product_id,customer)
{
    console.log("Add Cart Function Run ")
    console.log("Product ID is : ",product_id)
    console.log("Customer is ",customer)
    const data = { 
        product_id: product_id,
        action : action,
     };

    fetch('http://127.0.0.1:8000/update/', {
    method: 'POST', // or 'PUT'
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
    console.log('Success:', data);
    location.reload()
    })
    .catch((error) => {
    console.error('Error Ha:', error);
    });
}


