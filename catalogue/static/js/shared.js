$(document).ready(function() {

    var alertMessageElement = $(".alert");
    
	/* Modal window of ADD, EDIT */
	$("#add-btn").click(function(){
		$('#modify-window').modal();
		$('.modal-title').text("Добавить "+modal_title);
	});
    
    
    /* save object from modal window*/
    $("#save-object").click(function(){
        
        var invalidInputs = 0;
        
        $("form").find('input:text,textarea,select').each(function(index){ 
             
             var currElement = $(this);            
             
             /*
             In case of input:text and textareas the value is saved
             In case of select the option id is saved
             */
             if( currElement.get(0).tagName !== "SELECT"){
                                 
                 var isValid = true;
                 if(currElement.attr('required') === 'required'){
                     isValid = validateInput(this);
                 }
                 if(!isValid){
                    invalidInputs ++;
                 }
                 
             }
             
        });
        
        if(invalidInputs != 0){
            return false;
        }
        
     
        
	});

	/* Close aler messages */
	$(".close-btn").click(function (){
		alertMessageElement.hide();
	});


    /* Remove object */
	$(".remove-btn").click(function (){
                
            alertMessageElement.hide();
        
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
                            .animate( {backgroundColor:'#E8E8E8'}, 1000)
                                .fadeOut(1000,function() {
                                    $('#row_'+currentId).remove();
                        });
                                                
                        $("#super-cathegory-select option[id='cathegory_option_"+currentId+"']").remove();
                        
                        $("#info-message > span").html(success_msg);
                        $("#info-message").show();
                        
                    }else {
                        
                        $("#error-message > span").html(error_msg);
                        $("#error-message").show();
                    
                    }
                }
            );
      });
            

});

/*Validates text inputs. In case of error highlights the field*/
function validateInput(elem){

    var currElement = $(elem);
    var originalClass = currElement.attr('class');
    
    if (!currElement.val()) {
        
        currElement.attr({'class': originalClass + ' error-field'});
        return false;
    }
    
    var errorClassPosition = originalClass.lastIndexOf('error-field');
    if(errorClassPosition != -1){
        
        currElement.attr({'class': originalClass.substring(0,errorClassPosition)});
    }
    
    
    return true;
                 
}





