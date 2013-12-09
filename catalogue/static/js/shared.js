var alertMessageElement = $(".alert");
var modalWindow = $("#modify-window");
var object_type = $("#object-type").val();


$(document).ready(function() {
    
            
	/* Modal window of ADD, EDIT */
	$("#add-btn").click(function(){
		modalWindow.modal();
		$(".modal-title").text("Добавить "+modal_title);
	});
    
    
    
    
    
    /*
    Save object inserted in modal window 
    */
    $("#save-object").click(function(event){
                
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
                    isValid = validateInput(this, false);
                }
                
                /*
                It does not make sense to perform ajax request if input is empty
                */
                if(!isValid){
                        invalidInputs ++;
                }else{
                    
                    /*
                    Checking if field is already exists in database and could not be repeated
                    */
                    if(currElement.attr('class').lastIndexOf("no-repeat-field") != -1){
                
                        if( isFieldExists(this) ){
                            invalidInputs ++;
                        }
                        
                    }
                    
                }
                 
             }
            
             
        });
        
        /*
        If there was invalid inputs, the form action is not finished
        */
        if(invalidInputs != 0){
            return false;
        }
        
	});
    
    /* ------ Checks the database if the specific field exists ------- */
    /*$(".no-repeat-field").change(function(event) {
        isFieldExists(this);
    });*/
    

	/* ------ Close alert messages -------- */
	$(".close-btn").click(function (){
		alertMessageElement.hide();
	});


    /* ------- Remove object -----------*/
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
            
        $.post( "/ajax-catalogue/"+object_type+"/remove/", 
            {
                object_id:currentRemoveId
            },   
            function( data ) {
                var response = eval('(' + data + ')');

                if(response.status === 1){
                                        
                    $("#row_"+currentRemoveId)
                        .animate( {backgroundColor:'#E8E8E8'}, 500)
                            .fadeOut(500,function() {
                                $('#row_'+currentRemoveId).remove();
                    });
                                            
                    $("#super-category-select option[id='category_option_"+currentRemoveId+"']").remove();
                    
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
function validateInput(elem, isFieldExits){

    var currElement = $(elem);
    var originalClass = currElement.attr('class');
    var errorClassPosition = originalClass.lastIndexOf('error-field');
        
    if(errorClassPosition != -1){
        
        originalClass = originalClass.substring(0,errorClassPosition-1);
        currElement.attr({'class': originalClass});
    }
    
    if (!currElement.val() || isFieldExits === "true" ) {
                
        currElement.attr({'class': originalClass + ' error-field'});
        
        
        if(!currElement.val()){
            currElement.attr(
                "data-content", "Это поле не может быть пустым!"
            );
            currElement.popover("enable");
            currElement.popover("show");
            currElement.change(function(event) {
                currElement.popover("disable");
            });
        }
        
        return false;
    }
      
    return true;
                 
}

/* Ajax function that verifies if given element field exists in database */
function isFieldExists(element){
    
    var currElement = $(element);
    var fieldValue = currElement.val();
    var isFieldExists = false;
            
    $.ajaxSetup({async:false});//wait untill ajax responds
    $.get ( "/ajax-catalogue/"+object_type+"/valid-name/",
        {
            field_value:fieldValue
        },
        function ( data ) {
            
            var response = eval('(' + data + ')');
            validateInput(element, response.isExists);
            
            if( response.isExists === "true"){
                
                currElement.attr(
                    "data-content", $("#object-exists-message").val()
                );
                currElement.popover("enable");
                currElement.popover("show");
                currElement.change(function(event) {
                    currElement.popover("disable");
                });
                
                isFieldExists = true;
            }
            
        }
       
    );
    
    return isFieldExists;
    
}


/* 
When closing modal window, all input fields should be clean
*/
modalWindow.on("hidden.bs.modal", function () {
    
    $("form").find("input:text,textarea,select").each(function(index){
       
        /* 
        removing error shadowed fields
        */
        var currElement = $(this);
        var originalClass = currElement.attr('class');
        var errorClassPosition = originalClass.lastIndexOf("error-field");
        if(errorClassPosition != -1){
            originalClass = originalClass.substring(0,errorClassPosition-1);
            currElement.attr({'class': originalClass});
        }
        
        /* 
        cleaning inputs
        */
        currElement.val("");
        
        /* 
        removing popovers
        */
        currElement.popover("hide");
    });
    
});


