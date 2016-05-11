$(document).ready(function () {

  var SPINNER = '<i class="fa fa-spinner fa-pulse"></i>';
  var MUTABLE_SELECTS = $('select[download-on-click=1]');
  
  window['address_forms_count'] = window['address_forms_count'] || 0;
  var count = ++window['address_forms_count'];
  if (count > 1) {
    console.warn('[ Address Search ] %d search forms on a page', count);
    return false;
  }
  
  // Loading districts needs special behaviour to save previous value;
  function loadDistricts() {
    var elem_id = 'DISTRICT';

    var select = $('#' + elem_id);
    var label = $('label[for=' + elem_id + ']');

    //append_spinner
    label.append(SPINNER);

    //AJAX get
    var params = 'district=30&address=1';
    $.get(SELF_URL, params, function (data) {
        select.html(data);
        console.log(data)
      })
      .done(function () {
        label.find('i.fa').remove();
      });

  }

  function loadList(elem_id, param, value) {
      console.log(elem_id);
    var $select = $('#' + elem_id);
    var $label = $('label[for=' + elem_id + ']');
    //append_spinner
    $label.append(SPINNER);
    //AJAX get

    var params = 'qindex=30&address=1&' + param + '=' + value;
    $.get(SELF_URL, params, function (data) {
        $select.empty().html(data);
        $select.prop('disabled', false);
        $select.trigger("chosen:updated");
      })
      .done(function () {
        $label.find('i.fa').remove();
      });
  }

  function loadNext(elem_id) {
    switch (elem_id) {
      case 'DISTRICT':
        //load streets
        loadList('STREET', 'DISTRICT', getValue('DISTRICT'));
        break;
      case 'STREET':
        //load builds
        loadList('BUILD', 'STREET', getValue('STREET'));
        break;
    }
  }

  function clearNext(id) {

    switch (id) {
      case 'DISTRICT':
        //enable streets
        clearSelect('STREET');
        clearSelect('BUILD');
        break;
      case 'STREET':
        //enable builds
        clearSelect('BUILD');
        break;
    }
  }

  function getValue(elem_id) {
    return $('#' + elem_id).val();
  }

  function getSelect(elem_id) {
    return $('#' + elem_id);
  }

  function clearSelect(elem_id) {
    getSelect(elem_id).val('')
      .chosen(CHOSEN_PARAMS)
      .prop('disabled', true)
      .trigger("chosen:updated");

    $('#' + elem_id).val('');

    if (elem_id == 'BUILD') {
      $('#LOCATION').val('');
    }
  }

  var district = $('#DISTRICT').next('div');
  var streets = $('#STREET').next('div');

  //Register onClick handlers;
  MUTABLE_SELECTS.on('change', function () {
    //get value
    var $select = $(this);
    var value = $select.val();

    //update hidden
    var id = $select.attr('id');
    console.log("HERE " + id + " Val" + value);
    $('#' + id).val(value);
    console.log($('#' + id).val());

    if (id == 'BUILD') {
      $('#LOCATION').val(value);
    }

    clearNext(id);
    loadNext(id);
  });

  district.on('click', function () {
    getSelect('DISTRICT').trigger("chosen:updated");
  });

  //Allow loading streets before districts
  streets.one('click', loadStreetsWithoutDistricts);

  function loadStreetsWithoutDistricts() {
    var value = getValue('DISTRICT');
    console.log(value);
    if (value === '') {
      loadList('STREET', 'DISTRICT', '*');
    }
  }

  loadDistricts();

});