/* QLF main javascript
 *
 * @description     basic functions shared by the QLF project
 * @file            jquery.site.js
 * @author          Cristiano Singulani
 * @requirements    Jquery v1.11+ and Bootstrap v3.3+
 */

$.prototype.note = function(message, options) {

    var buttons = [];
    var alarm = "danger"

    console.log(options)

    if (options.alarm) {
        console.log(options.alarm)
        alarm = options.alarm;
    }

    var main_class = "alert alert-" + alarm;

    if (Array.isArray(options.buttons)) {
        buttons = options.buttons;
    };

    if ((options.classes) && (options.classes.fade_in) && (buttons.length < 1)) {
        main_class = main_class + " fade in";
    };

    var div = $("<div>");
    div.attr("class", main_class);

    var button = $("<button>");
    button.attr("type", "button");
    button.attr("class", "close");
    button.attr("data-dismiss", "alert");
    button.attr("aria-label", "Close");

    var span = $('<span aria-hidden="true">&times;</span>');

    button.append(span);

    var strong = $("<strong>");
    strong.append(message);

    div.append(button);
    div.append(strong);

    $(this).empty().append(div);

    for (x=0; x < buttons.length ; x++){
        var btn = buttons[x];

        var btn_html = $("<button>");
        btn_html.attr("type", "button");
        btn_html.attr("class", "btn-alert btn btn-" + alarm);

        btn_html.html(btn.legend).on('click', btn.trigger);
        div.append(btn_html);
    }

    if ((options.classes) && (options.classes.fade_in) && (buttons.length < 1)) {
        $(div).fadeTo(5000, 0.25, function() {
            $(this).remove();
        });
    };

}
