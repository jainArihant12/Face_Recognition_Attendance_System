const form = document.querySelector('.login-in')
const button = document.querySelector('.login')
const closebtn = document.querySelector('.fa-xmark')


button.addEventListener('click', function() {
    
    form.classList.add('active-popup')
  });

  
closebtn.addEventListener('click' , ()=>{
    form.classList.remove('active-popup');
}
)
