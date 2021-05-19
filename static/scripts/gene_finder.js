$(document).ready(function (){
    var max_input_fields = 6
    var wrapper = $(".input_wrapper")
    var add_button = $("#add_button")

    var counter = 1
    $(add_button).click(function (e){
        e.preventDefault()
        if(counter < max_input_fields) {
            counter++
            $(wrapper).append('<div><input class="form-control input-block mt-2" type="text" name="and"><button class="btn btn-danger mt-2 mb-2 float-right" id="remove_button" type="button">-</button></div>')
        }
    })

    $(wrapper).on("click", "#remove_button", function (e){
        e.preventDefault()
        $(this).parent('div').remove()
        counter--
    })

})

$(document).ready(function (){
    var max_input_fields = 6
    var wrapper = $(".input_wrapper_OR")
    var add_button = $("#add_button_OR")

    var counter = 1
    $(add_button).click(function (e){
        e.preventDefault()
        if(counter < max_input_fields) {
            counter++
            $(wrapper).append('<div><input class="form-control input-block mt-2" type="text" name="or"><button class="btn btn-danger mt-2 mb-2 float-right" id="remove_button" type="button">-</button></div>')
        }
    })

    $(wrapper).on("click", "#remove_button", function (e){
        e.preventDefault()
        $(this).parent('div').remove()
        counter--
    })

})


