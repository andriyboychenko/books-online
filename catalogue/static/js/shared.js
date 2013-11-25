$(document).ready(function() {

	/* Modal window of ADD, EDIT */
	$("#add_btn").click(function(){
		$('#modify_window').modal();
		$('.modal-title').text("Добавить "+modal_title);
	});



	/* Close aler messages */
	$(".close_btn").click(function (){
		$(".alert").hide();
	});


	$(".remove-btn").click(function (){
                
                $(".alert").hide();
            
                var currentId = $(this).attr('id');
                
                $.post( "/ajax_catalogue/remove/", 
                    {
                        object_id:currentId,
                        object_type:object_type
                    },   
                    function( data ) {
                        var response = eval('(' + data + ')');

                        if(response.status === 1){
                                                
                            $("#row_"+currentId)
                                .animate( {backgroundColor:'#FFFF99'}, 1000)
                                    .fadeOut(1000,function() {
                                        $('#row_'+currentId).remove();
                            });
                            
                            $("#info_message > span").html(success_msg);
                            $("#info_message").show();
                            
                        }else {
                            
                            $("#error_message > span").html(error_msg);
                            $("#error_message").show();
                        
                        }
                    }
                );
          });
            

});
            
