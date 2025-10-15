const addButtons = document.getElementsByClassName('add-button');
const subButtons = document.getElementsByClassName('sub-button');
const qtyInputs = document.getElementsByClassName('qty-input');
const resDateTime = document.getElementById('reservation-datetime');
const pickUpTime = document.getElementById('pickup-time');
const pickUpWarning = document.getElementById('pickup-warning');
const dateTimeWarning = document.getElementById('reservation-warning');
const dishDivs = document.getElementsByClassName('card');
const totalHeading = document.getElementById('total-heading');
const subtotalHeadings = document.getElementsByClassName('review-card-subtotal');


//Adds listeners to all +/- buttons and connect them to the corresponding quantity input feild and updates total on menu page
function quantityHelper(input){
    return parseInt(qtyInputs[input].value)
}
function priceHelper(input){
    return parseFloat(dishDivs[input].dataset.price);
}
let total = 0;
function updateTotal(input=0, operation) {
    if(operation='refresh'){
        total = 0;
        for(let i = 0; i < dishDivs.length; i++){
            total += quantityHelper(i) * priceHelper(i)
            total = parseFloat(total.toFixed(2))
        }
    }else{
        if (operation == 'add') {
            total += parseFloat(dishDivs[input].dataset.price);
        }else{
            total -= parseFloat(dishDivs[input].dataset.price);
        }
    }
    return parseFloat(total.toFixed(2));
}
totalHeading.innerHTML = updateTotal('refresh');
function updateSubtotal(input){
    let subtotal = quantityHelper(input) * priceHelper(input)
    return subtotal.toFixed(2);
}
for(let i = 0; i < addButtons.length; i++){
    addButtons[i].addEventListener('click', function(){
        qtyInputs[i].value = quantityHelper(i) + 1;
        totalHeading.innerHTML = updateTotal(i, 'add');
        subtotalHeadings[i].innerHTML = updateSubtotal(i);
    });
    subButtons[i].addEventListener('click', function(){
        if(qtyInputs[i].value != '0'){
            qtyInputs[i].value = quantityHelper(i) - 1;
            totalHeading.innerHTML = updateTotal(i, 'sub');
            subtotalHeadings[i].innerHTML = updateSubtotal(i);
        }

    })
    qtyInputs[i].addEventListener('change', function(){
        if(!quantityHelper(i)){
            qtyInputs[i].value = 0;
        }
        totalHeading.innerHTML = updateTotal('refresh');
        subtotalHeadings[i].innerHTML = updateSubtotal(i);
    })
}

//Set and validate that datetime input value is larger than current time in Amman
//Creates a date object that is based on current UTC time and then adds "X" hours * 3600 seconds * 1000ms to adjust for timezone
function dateHelper(plusUTC){
    return new Date(Date.now() + 3600 * 1000 * plusUTC)
}
//Converts the date to YYYY-mm-ddTHH:MM:SS... string format (ISO string) and slices it between post1 and pos2
function dateSlicer(date, pos1, pos2){
    return date.toISOString().slice(pos1, pos2);
}
//Compares Date.now() UTC+3 (Amman) to input to determine if the reservation time is in the past
if(resDateTime){
    //Set value at page load to now()
    let dateTimeNow = dateSlicer(dateHelper(3),0,16);
    resDateTime.value = dateTimeNow;
    resDateTime.addEventListener('change', function(){
        if(Date.parse(resDateTime.value) < Date.now()){
            //Recalculate on change to keep now() current
            dateTimeNow = dateSlicer(dateHelper(3),0,16);
            resDateTime.value = dateTimeNow;
            dateTimeWarning.innerHTML = "(cannot be in the past)";
        } else{
            dateTimeWarning.innerHTML = "";
        }
    })
}

//Set and validate that time input is at least 1 hour in the future from current time in Amman
//Converts time HH:MM string into an int by multiplying HH by 60 and then adding it to MM
function timeHelper(time){
    return parseInt(time.slice(0, 2))*60+parseInt(time.slice(3));
}
//Compares time input with current time in Amman + 1 hour (UTC+4)
if(pickUpTime){
    //Set value at page load to now()
    let timeNow = dateSlicer(dateHelper(4),11,16);
    pickUpTime.value = timeNow;
    pickUpTime.addEventListener('change', function(){
        //Recalculate on change to keep now() current
        timeNow = dateSlicer(dateHelper(4),11,16);
        const inputTime = timeHelper(pickUpTime.value)
        if(timeHelper(timeNow) > inputTime){
            pickUpTime.value = timeNow;
            pickUpWarning.innerHTML = "(minimum 1 hour processing time)";
        }
        else{
            pickUpWarning.innerHTML = "";
        };
})
}