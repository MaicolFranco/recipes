function addItem(){
    var Item = document.querySelector('#ingredients .item').innerHTML;
    var newItem = '<div class="row item">' + Item + '</div>';
    var form = document.querySelector('.items');
    form.insertAdjacentHTML('beforeend', newItem);
    console.log(newItem);
}

function removeItem(){
    var list = document.querySelector(".items");
    list.removeChild(list.lastChild);
}