
var modal = document.getElementById("myModal");
var btn = document.getElementById("delete_auction");
var span = document.getElementsByClassName("close")[0];
var exit = document.getElementById('exit')
var confirm = document.getElementById('yes')
function DeleteAuction(value)
{

    modal.style.display = "block";
    confirm.onclick = function ()
    {
        xhr = new XMLHttpRequest()
        xhr.open('GET', '/transactions/auction-remove/' + value.value, true)
        xhr.onload = function ()
        {
            if (this.status == 200)
            {
                console.log(this.responseText)
                modal.style.display = 'none'
                location.reload()
            }
        }
        xhr.send()
    }

    span.onclick = function ()
    {
        modal.style.display = "none";
    };
    exit.onclick = function ()
    {
        modal.style.display = "none";
    };
    window.onclick = function (event)
    {
        if (event.target == modal)
        {
            modal.style.display = "none";
        }
    };
}