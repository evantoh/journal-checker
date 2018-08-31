function updateElementIndex1(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.credit) el.credit = el.credit.replace(id_regex, replacement);
}

function cloneMore1(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var credit = $(this).attr('credit')
        if (credit) {
            credit = credit.replace('-' + (total - 1) + '-', '-' + total + '-');
            var id = 'id_' + credit;
            $(this).attr({
                'credit': credit,
                'id': id
            }).val('').removeAttr('checked');
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row1:not(:last)');
    conditionRow.find('.btn.add-form-row1')
        .removeClass('btn-success').addClass('btn-danger')
        .removeClass('add-form-row1').addClass('remove-form-row1')
        .html('-');
    return false;
}

function deleteForm1(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1) {
        btn.closest('.form-row1').remove();
        var forms = $('.form-row1');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find(':input').each(function() {
                updateElementIndex1(this, prefix, i);
            });
        }
    }
    return false;
}
$(document).on('click', '.add-form-row1', function(e) {
    e.preventDefault();
    cloneMore1('.form-row1:last', 'form');
    return false;
});
$(document).on('click', '.remove-form-row1', function(e) {
    e.preventDefault();
    deleteForm1('form', $(this));
    return false;
});