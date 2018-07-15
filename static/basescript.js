function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
modal=document.getElementById("mysearch");
 function search(){

   var query=$('#txtbox').val();
   if(query=="")
    {
    $('.searchresults').html("");
    }
    else
    {
    document.getElementById("mysearch").style.display = "block";
    $.ajax(
    {
        type:"GET",
        dataType:'json',
        url: "/api/search",
        data:{
                 query:query,

        },
        success: function( data )
        {
            var tab=$('<div />');
          for(var i=0;i<data.length;i++)
          {
          tab.append('<p class="srchbckgd"');
          var uid=data[i].id;
           $('<a />', {value: data[i].username, text: data[i].username,id:"user"+data[i].id,href:"https://facebook-clone-app.herokuapp.com/view_profile/"+uid}).appendTo(tab);
           tab.append('</p>');

          }

          $('.searchresults').html(tab);
        },
        error: function(jqXHR, textStatus, errorThrown){
          alert('error');
      }
     })
     }
    }

      window.onclick = function(event) {
    document.getElementById("mysearch").style.display = "none";
}
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
     $('.addfriend').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.ajax(
    {
        type:"GET",
        url: "/requestfriend",
        data:{
                 friend_id: catid
        },
        success: function( data )
        {
            $( '#add_frnd'+ catid ).text("Requested");
            $('#add_frnd'+ catid).prop('disabled', true);
        }
     })
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


   $('.displaycmnts').click(function(){
    catid = $(this).attr("data-catid");
    $('#comments'+catid).toggle();
    });
