var index=0;
Carousel();
function Carousel()
{
    var i;

    var x = document.getElementsByClassName('pic1');
    for(i=0; i<x.length; i++)
    {
        if(i==index)
        {
            x[i].style.display = "block";
        }
        else{
            x[i].style.display = "none";
        }
    }
    index++;
    if(index>=x.length)
    {
        index = 0;
    }
    setTimeout(Carousel,100);
}
