const addButtons = document.getElementsByClassName('add-button');
const subButtons = document.getElementsByClassName('sub-button');
const qtyInputs = document.getElementsByClassName('qty-input');
const resDateTime = document.getElementById('reservation-datetime');
const pickUpTime = document.getElementById('pickup-time')

for(let i = 0; i < addButtons.length; i++){
    addButtons[i].addEventListener('click', function(){
        qtyInputs[i].value = parseInt(qtyInputs[i].value) + 1;
    });
    subButtons[i].addEventListener('click', function(){
        if(qtyInputs[i].value != '0'){
            qtyInputs[i].value = parseInt(qtyInputs[i].value) - 1;
        }
    })
}

//Check if datetime input value is larger than current time in Amman
function dateHelper(plusUTC){
    return new Date(Date.now() + 3600000 * plusUTC)
}
function dateSlicer(date, pos1, pos2){
    return date.toISOString().slice(pos1, pos2);
}
if(resDateTime){
    resDateTime.addEventListener('change', function(){
        //Adjust Date.now() to UTC+3 (Amman) by adding 3 hours * 3600 seconds * 1000 ms
        if(Date.parse(resDateTime.value)< (Date.now() + 3600000 * 3)){ 
            const timeNowObject = dateSlicer(dateHelper(3),0,10);
            resDateTime.value = timeNowObject;
    }
})
}

//Check if time input is at least 1 hour in the future from current time in Amman
function timeHelper(time){
    return parseInt(time.slice(0, 2))*60+parseInt(time.slice(3));
}

if(pickUpTime){
    pickUpTime.addEventListener('change', function(){
        const timeNow = dateSlicer(dateHelper(4),11,16);
        const inputTime = timeHelper(pickUpTime.value)
        if(timeHelper(timeNow) > inputTime){
            pickUpTime.value = timeNow;
        };
})
}