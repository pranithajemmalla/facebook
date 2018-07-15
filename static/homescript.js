 $('.cmtinput').keypress(function(ev){

    if(ev.key==="Enter")
    {

    catid = $(this).attr("data-catid");
    var txtbox=$('#textbox'+catid).val();
    document.getElementById('textbox'+catid).value = "";
    $('#pcomment'+catid).append("<p>"+txtbox+"</p>");
    $.ajax(
    {
        type:"GET",
        url: "/addcomment",
        data:{
                 post_id: catid,
                 comment: txtbox,
        },
        success: function( data )
        {

        }
     })
     }
    });

    $('.likebutton').click(function(){
    var catid,data1="aa";
    $(this).toggleClass('liked');
    catid = $(this).attr("data-catid");
    $.ajax(
    {
        type:"GET",
        url: "/likepost",
        data:{
                 post_id: catid,

        },
        success: function( data )
        {

          document.getElementById('likecnt'+catid).innerHTML = data+" Likes";

        },
        error: function(jqXHR, textStatus, errorThrown){
          alert('error');
      }
     })
    });


   $('.deletepost').click(function(){
    catid = $(this).attr("data-catid");
    $.ajax(
    {
        type:"GET",
        url: "/deletepost",
        data:{
                 pid: catid
        },
        success: function( data )
        {
            document.getElementById('postid'+catid).style.display="none";
        }
     })
});
     $('.displaycmnts').click(function(){
    catid = $(this).attr("data-catid");
    $('#comments'+catid).toggle();
    });