$(document).ready(function () {
  let table;
  const input_date = $("#input_date");
  const input_time = $("#input_time");
  const input_interval = $("#input_interval");
  const input_text = $("#input_text");

  let now = new Date();
  let day = now.getDate();
  let day_of_week = now.getDay();
  let diff = 1;
  if (day_of_week === 7) {
    diff = 2;
  } else if (day_of_week === 1) {
    diff = 3;
  }
  now.setDate(day - diff);
  input_date.val(now.toISOString().slice(0, 10));


  function create_table() {
    const url = "empty/";
    table = $("#esmo_table").DataTable({
      scrollX: true,
      lengthMenu: [
        [20, -1],
        [20, "Все"],
      ],
      DisplayLength: -1,
      paging: true,
      order: [[3, "desc"]],
      language: {
        url: "static/plug-ins/9dcbecd42ad/i18n/Russian.json",
      },
      processing: true,
      ajax: {
        url: url,
        dataSrc: "",
      },
      columns: [
        { data: "number" },
        { data: "name" },
        { data: "division" },
        { data: "type_1[</br>]" },
        { data: "type_2[</br>]" },
        { data: "duration[</br>]" },
        { data: "marks", visible: false },
      ],
    });



    $("#esmo_table tbody").on("click", "tr", function () {
      if ($(this).hasClass("selected")) {
        $(this).removeClass("selected");
      } else {
        table.$("tr.selected").removeClass("selected");
        $(this).addClass("selected");
      }
    });

  }

  $("#TableButton").on("click", function () {
    input_text.val(`Дата: ${input_date.val()} Время: ${input_time.val()} Интервал: ${input_interval.val()}`);
    const url = `api/?date=${input_date.val()}&time=${input_time.val()}&interval=${input_interval.val()}`;
    if (table) {
      table.ajax.url(url).load();
    } else {
      create_table();
    }
  });

create_table();
});