$(document).ready(function() {

    var alertMessageElement = $(".alert");
    var modalWindow = $('#modify-window');
    
	/* Modal window of ADD, EDIT */
	$("#add-btn").click(function(){
		modalWindow.modal();
		$('.modal-title').text("Добавить "+modal_title);
	});
    
    /* When closing modal window, all input fields should be clean*/
    modalWindow.on('hidden.bs.modal', function () {
        
        $("form").find("input:text,textarea,select").each(function(index){
            $(this).val("");
        });
    });
    
    
    /* save object from modal window*/
    $("#save-object").click(function(){
        
        var invalidInputs = 0;
        
        $("form").find("input:text,textarea,select").each(function(index){ 
             
             var currElement = $(this);            
             
             /*
             In case of input:text and textareas the value is saved
             In case of select the option id is saved
             */
             if( currElement.get(0).tagName !== "SELECT"){
                                 
                 var isValid = true;
                 if(currElement.attr("required") === "required"){
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


    /* -------Remove object -----------*/
    var currentRemoveId;
	$(".remove-btn").click(function (){
        
        currentRemoveId = $(this).attr('id');

        alertMessageElement.hide();
            
        $(".remove-object-name").html(
            $("#remove-confirmation-object-name").val()
        );
        $("#remove-confirmation-window").modal();        
            
        
    });
    
    $("#remove-confirm-object").click(function (){
            
        $.post( "/ajax_catalogue/remove/", 
            {
                object_id:currentRemoveId,
                object_type:object_type
            },   
            function( data ) {
                var response = eval('(' + data + ')');

                if(response.status === 1){
                                        
                    $("#row_"+currentRemoveId)
                        .animate( {backgroundColor:'#E8E8E8'}, 500)
                            .fadeOut(500,function() {
                                $('#row_'+currentRemoveId).remove();
                    });
                                            
                    $("#super-cathegory-select option[id='cathegory_option_"+currentRemoveId+"']").remove();
                    
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





