$(document).ready(function () {
  let table;
  const input_date = $("#input_date");
  const input_time = $("#input_time");
  const input_interval = $("#input_interval");
  const input_text = $("#input_text");
  const select_div = $("#select_div");

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

  async function get_data(url_request) {
    return $.ajax({
      type: "GET",
      url: url_request,
      success: function (response) {
        response;
      },
    });
  }

  async function get_divs() {
    let divs = await get_data("/divs");
    select_div.empty();
    select_div.append(`<option value="0">Все</option>`);
    for (let i = 0; i < divs.length; i++) {
      select_div.append(
        `<option value="${divs[i]["id"]}">${divs[i]['name']}</option>`
      );
    }
  }


  function create_table() {
    const url = "empty/";
    table = $("#esmo_table").DataTable({
      scrollX: true,
      lengthMenu: [
        [5, 10, 20, -1],
        [5, 10, 20, "Все"],
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
    let interval = input_interval.val();
    if (interval > 48) {
      interval = 48;
    } else if (interval < 0) {
        interval = 0;
    }
    input_text.val(
        `Дата: ${input_date.val()}
         Время: ${input_time.val()}
         Интервал: ${interval}
         Подразделение: ${select_div.find(":selected").text()}`
    );
    let url = `/exams/?date=${input_date.val()}&time=${input_time.val()}&interval=${interval}`;
    console.log(select_div.val());
    if (select_div.val() !== "0") {
      url += `&div=${select_div.val()}`;
    }

    console.log(url);
    if (table) {
      table.ajax.url(url).load();
    } else {
      create_table();
    }
  });

  async function main() {
    await get_divs();
    create_table();
  }

  main();
});