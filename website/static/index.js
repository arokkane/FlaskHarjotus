function deleteNote(noteId){
    fetch("/delete-note",{
        method: "POST",
        body: JSON.stringify({noteId: noteId})
    }).then((_res) =>{
        window.location.href = "/";
    })
}
$(document).ready(function(){
    $('.application').click(function(){
        console.log("click detected")
        var userid = $(this).data('id');
        console.log(userid)
        $.ajax({
            url: '/applicantdata',
            type: 'post',
            data: {userid: userid},
            success: function(data){ 
                $('.modal-body').html(data); 
                $('.modal-body').append(data.htmlresponse);
                $('#applyModal').modal('show'); 
            }
        });
    });
});