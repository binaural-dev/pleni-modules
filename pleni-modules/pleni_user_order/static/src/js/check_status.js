let elem = document.getElementById('status-path');
let step2 = document.getElementById('step2');
let step3 = document.getElementById('step3');
let step4 = document.getElementById('step4');
let step5 = document.getElementById('step5');

if (elem.value) {
    if (['waiting', 'confirmed'].includes(elem.value)) {
        step2.classList.add("active")
    } else if (['assigned'].includes(elem.value)) {
        step2.classList.add("active")
        step3.classList.add("active")
        step4.classList.add("active")
    } else if (['done'].includes(elem.value)) {
        step2.classList.add("active")
        step3.classList.add("active")
        step4.classList.add("active")
        step5.classList.add("active")
    }
}


setTimeout(function(){
    //     //Ordenes de Entrega - change
    let selector = document.querySelectorAll('.o_sale_stock_picking')
    selector.forEach( (item, index) => {
        item.classList.remove("d-flex")
        item.style.display = "none";
    })

    let delivery_child = document.getElementById('informations').children
    let delivery_child_length = delivery_child.length
    let delivery_child_count = 0

    for(delivery_child_count ; delivery_child_count < delivery_child_length ; delivery_child_count++){
        let child = delivery_child[delivery_child_count]
        if (child.innerHTML.includes("Órdenes de Entrega")) {
            child.style.display = "none";
        }
    }
    
}, 100);