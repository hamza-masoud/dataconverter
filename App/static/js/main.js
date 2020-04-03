function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(element).text()).select();
    document.execCommand("copy");
    alert("the text was copied");
    $temp.remove();
}


function sel() {
    show = document.querySelectorAll('.inputGroupSelect');

    for (x = 0; x <= (show.length - 1); x++) {
        show[x].style.display = 'inline-block';
    }
    val = document.querySelector('#inputGroupSelect01').value;

    switch (val) {
        case 'json':
            inp = document.querySelector('#inputGroupcheckbox01');
            inpl = document.querySelector('#inputGroupcheckbox01l');

            inp.style.display = 'none';
            inpl.style.display = 'none';
            break;


        case 'csv':
            inp = document.querySelector('#inputGroupcheckbox02');
            inpl = document.querySelector('#inputGroupcheckbox02l');

            inp.style.display = 'none';
            inpl.style.display = 'none';
            break;


        case 'txt':
            inp = document.querySelector('#inputGroupcheckbox03');
            inpl = document.querySelector('#inputGroupcheckbox03l');

            inp.style.display = 'none';
            inpl.style.display = 'none';
            break;

        /*case 'xlsx':
        *    inp = document.querySelector('#inputGroupcheckbox04');
        *    inpl = document.querySelector('#inputGroupcheckbox04l');
*
 *           inp.style.display = 'none';
  *          inpl.style.display = 'none';
            break;
    */
    }
}