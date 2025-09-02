function setCountry(code) {
    if (code || code == '') {
        var text = jQuery('a[cunt_code="' + code + '"]').html();
        $(".country-wrapper .dropdown dt a span").html(text);
    }
}
$(document).ready(function () {
    $(".country-wrapper .dropdown img.flag").addClass("flagvisibility");

    $(".country-wrapper .dropdown dt a").click(function () {
        $(".dropdown dd ul").toggle();
    });

    $(".country-wrapper .dropdown dd ul li a").click(function () {
        //console.log($(this).html())
        var text = $(this).html();
        $(".country-wrapper .dropdown dt a span").html(text);
        $(".country-wrapper .dropdown dd ul").hide();
        $(".country-wrapper #result").html("Selected value is: " + getSelectedValue("country-select"));
    });

    function getSelectedValue(id) {
        //console.log(id,$("#" + id).find("dt a span.value").html())
        return $("#" + id).find("dt a span.value").html();
    }

    $(document).bind('click', function (e) {
        var $clicked = $(e.target);
        if (!$clicked.parents().hasClass("dropdown"))
            $(".country-wrapper .dropdown dd ul").hide();
    });


    $(".country-wrapper #flagSwitcher").click(function () {
        $(".country-wrapper .dropdown img.flag").toggleClass("flagvisibility");
    });
});