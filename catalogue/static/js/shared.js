
$(document).ready(function () {
        
    var alertMessageElement = $(".alert");
    var modalWindow = $("#modify-window");
    
	/* Modal window of ADD */
	$("#add-btn").click(function () {
        
        var modal_title = $("#modal-title-add-message").val();

        /* some pages do not have add/edit modal windows, for example book-management*/
        if (modal_title === "false") {
            return false;            
        }
        
        $(".modal-title").text(modal_title);
        modalWindow.modal();
                        
	});
    
    
    /* Modal window of EDIT */
    $(".edit-btn").click(function () {
        
        var currentEditId = $(this).attr('id');
        var modal_title = $("#modal-title-edit-message").val();
        
        if (modal_title === "false") {
            return false;            
        }
        		        
        $(".modal-title").text(modal_title);
        $("#edit-id").val(currentEditId);
        
        modalWindow.modal();
                
        $.get("/ajax-catalogue/" + object_type + "/edit-load-data/",
            {
                current_id: currentEditId
            },
            function (data) {

                var response = eval('(' + data + ')')[0];
                
                switch (object_type) {
                    case "bookcategory":
                        $("[name='book-category-name-txt']").val(response.fields.category_name);
                        $("[name='book-category-desc-txt']").val(response.fields.category_description);
                        $("[name='super-category-select']").val(response.fields.sub_category_of);
                        $("#category_option_" + response.pk).hide();
                        break;
                    case "bookattribute":
                        $("[name='book-attribute-name-txt']").val(response.fields.attribute_name);
                        $("[name='book-attribute-desc-txt']").val(response.fields.attribute_description);
                        break;
                    default:
                        alert("TODO: woops!");
                        break;
                }
                
               
            })
        .error(function () {alert('TODO: woops!'); });
    });
    
    
    
    /*
    Save object inserted in modal window 
    */
    $("#save-object").click(function (event) {
                        
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
                
                        if(isFieldExists(this)){
                            invalidInputs += 1;
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
    var attributeType = $("#attribute-type").val();
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
                object_id:currentRemoveId,
                attribute_type:attributeType
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
        
    
    /* 
     * When closing modal window, all input fields should be clean
     */
    modalWindow.on("hidden.bs.modal", function () {
        
        $("form").find("input:text,textarea,select").each(function(index) {
           
            /* 
             * removing error shadowed fields
             */
            var currElement = $(this);
            var originalClass = currElement.attr('class');
            var errorClassPosition = originalClass.lastIndexOf("error-field");
            if(errorClassPosition != -1) {
                originalClass = originalClass.substring(0,errorClassPosition-1);
                currElement.attr({'class': originalClass});
            }
            
            /* 
             * cleaning inputs
             */
            currElement.val("");
            
            /* 
             * removing popovers
             */
            currElement.popover("hide");
            
            /*
             * in case of editiong book category we need to show
             * hidden current book category
             */
            $("#super-category-select option").show();
        });
        
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
    var currentEditId = $("#edit-id").val();
    var attributeType = $("#attribute-type").val();
    var isFieldExists = false;
            
    $.ajaxSetup({async:false});//wait untill ajax responds
    $.get ( "/ajax-catalogue/"+object_type+"/valid-name/",
        {
            field_value: fieldValue,
            edit_id: currentEditId,
            attribute_type: attributeType
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




