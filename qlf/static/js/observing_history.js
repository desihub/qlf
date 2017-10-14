/* Observing History interface
 *
 * @description     javascript manipulation on the Observing History interface.
 * @file            observing_history.js
 * @author          Cristiano Singulani
 * @requirements    Jquery v1.11+ and Bootstrap v3.3+
 */

$(document).ready(function() {

    table = $('#exposures_table').ObservHistTable();

    $('.input-daterange').on('changeDate', function(ev){
        table.draw();
    } );

    $('#btn-manual-exec').click( function () {

        $('#alert-manual-exec div.alert').alert('close');
        var exposures = table.getSelected();

        if (exposures.length > 0) {

            $.ajax( {
                url: '/daemon_status/',
                dataType: 'json',
                success: function(data) {
                    if( data.status ) {

                        var options = { classes: { fade_in: true } };
                        var options = {};

                        $("#alert-manual-exec").note(
                            data.message,
                            options
                        );

                    } else {
                        console.log('Running manual mode...');

                        $.ajax( {
                            url: '/run_manual_mode/',
                            data: { 'exposures': exposures },
                            dataType: 'json',
                            success: function(data) {

                                if (!data['success']) {
                                    $("#alert-manual-exec").note(
                                        data['message']
                                    );
                                    return false
                                }

                                window.open('/dashboard/monitor/', 'monitorAPP', 'toolbar=0,location=0,menubar=0').focus();

                                $("#alert-manual-exec").note(
                                    data['message'],
                                    {'alarm': 'success'}
                                );

                                return true
                            }
                        } );

                    }
                }
            } );

        } else {

            var options = { classes: { fade_in: true } };
            var options = {};

            $("#alert-manual-exec").note(
                "Please select at least one exposure.",
                options
            );

        }

    } );

} );

$.prototype.ObservHistTable = function() {

    var selected_exposures = [];

    var exposures_table = $(this).DataTable( {
        "processing": true,
        "serverSide": true,
        // "lengthMenu": [[1, 5, 10], [1, 5, 10]],
        "ajax": $.fn.dataTable.pipeline( {
            "url": "/dashboard/api/datatable_exposures/",
            "data": function(extra){
                var daterange = $('.input-daterange');
                extra.start_date = daterange.find('input[name="start"]').val()
                extra.end_date = daterange.find('input[name="end"]').val()
            },
            "pages": 5,
            "type": "GET"
        } ),
        "columns": [
            {"data": function(row){
                var dateobs = new Date(row.dateobs);
                var mm = dateobs.getUTCMonth() + 1; // getMonth() is zero-based
                var dd = dateobs.getUTCDate();
                var hh = dateobs.getUTCHours();
                var min = dateobs.getUTCMinutes();

                return [
                    dateobs.getUTCFullYear(), '-',
                    (mm>9 ? '' : '0') + mm, '-',
                    (dd>9 ? '' : '0') + dd, ' ',
                    (hh>9 ? '' : '0') + hh, ':',
                    (min>9 ? '' : '0') + min, 'H'
                ].join('')
            }},
            {"data": "exposure_id"},
            {"data": "tile"},
            {"data": "telra"},
            {"data": "teldec"},
            {"data": "exptime"},
            {"data": function(row){return '-'}},
            {"data": function(row){return '-'}},
            /*{"data": "flavor"},*/
            {"data": "airmass"},
            {"data": function(row){return '-'}},
            {"data": function(row){return '-'}},
            {"data": function(row){return '-'}}
        ],
        "columnDefs": [
            { className: "text-nowrap", "targets": [ 0 ] }
        ]
    } );

    $(this).find('tbody').on( 'mouseenter', 'td', function () {

        var colIdx = exposures_table.cell(this).index().column;

        $( exposures_table.cells().nodes() ).removeClass( 'highlight' );
        $( exposures_table.column( colIdx ).nodes() ).addClass( 'highlight' );

    } );

    $(this).find('tbody').on( 'click', 'tr', function () {

        $(this).toggleClass('selected');

        var item = exposures_table.row( this ).data();
        var exposure_id = item.exposure_id;

        if ( $(this).hasClass('selected') ) {

            if ($.inArray(exposure_id, selected_exposures) < 0) {
                selected_exposures.push(item.exposure_id)
            }

        } else {

            if ($.inArray(exposure_id, selected_exposures) > -1) {
                var index = selected_exposures.indexOf(exposure_id);
                selected_exposures.splice(index)
            }

        }

    } );

    exposures_table.on( 'draw', function () {

        $.each( exposures_table.rows().nodes(), function ( i, node ) {

            var item = exposures_table.row( node ).data();

            $.each( selected_exposures, function ( i, exposure_id ) {

                if (item.exposure_id == exposure_id) {
                    $(node).addClass('selected');
                }

            } );

        } );

    } );

    this.getSelected = function() {
        return selected_exposures;
    }

    this.getTable = function() {
        return exposures_table;
    }

    this.draw = function() {
        exposures_table.clearPipeline().draw();
    }

    return this;

}