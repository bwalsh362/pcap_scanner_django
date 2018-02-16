$(document).ready(function() {
    $('table').each(function () {
        var $table = $(this);

        var $button = $("<button type='button' class='btn btn-default'>");
        $button.text("Export Table to CSV");
        $button.insertAfter($table);

        $button.click(function () {
            var csv = $table.table2CSV({
                delivery: 'value'
            });
            window.location.href = 'data:text/csv,'
            + encodeURIComponent(csv);

        });
        var $pdf_button = $("<button type='button' class='btn btn-default'>");
        $pdf_button.text("Export Table to PDF");
        $pdf_button.insertAfter($table);

        $pdf_button.click(function () {
            var pdf = new jsPDF('p', 'pt', 'letter');
            source = $('#table-section')[0];
            specialElementHandlers = {
                '#bypassme': function (element, renderer) {
                    return true
                }
            };
            margins = {
                top: 80,
                bottom: 60,
                left: 40,
                width: 522
            };
            pdf.fromHTML(
                source,
                margins.left,
                margins.top, {
                    'width': margins.width,
                    'elementHandlers': specialElementHandlers
                },
                function (dispose) {
                    pdf.save('Test.pdf');
                }
                , margins
            );
        })
    });
});
