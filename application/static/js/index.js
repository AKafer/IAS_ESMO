$(document).ready(function () {
  let table;
  const input_date = $("#input_date");
  const input_time = $("#input_time");
  const input_interval = $("#input_interval");
  const input_text = $("#input_text");

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

create_table();

  $("#TableButton").on("click", function () {
      console.log(input_date.val());
      console.log(input_time.val());
      console.log(input_interval.val());
      input_text.val(`Дата: ${input_date.val()} Время: ${input_time.val()} Интервал: ${input_interval.val()}`);
      const url = `api/?date=${input_date.val()}&time=${input_time.val()}&interval=${input_interval.val()}`;
      if (table) {
        table.ajax.url(url).load();
      } else {
        create_table();
      }


  //   const selectedFile = document.querySelector("#input_csv").files[0];
  //   console.log(selectedFile);
  //   console.log($("#input_csv").val());
  //
  //   csrftoken = window.CSRF_TOKEN;
  //   function csrfSafeMethod(method) {
  //     // these HTTP methods do not require CSRF protection
  //     return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  //   }
  //   $.ajaxSetup({
  //     beforeSend: function (xhr, settings) {
  //       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
  //         xhr.setRequestHeader("X-CSRFToken", csrftoken);
  //       }
  //     },
  //   });
  //
  //   var data = new FormData();
  //   data.append("file", selectedFile);
  //   console.log("datA", data);
  //
  //
  //
  //   $.ajax({
  //     type: "POST",
  //     url: "api/files/",
  //     data: data,
  //     processData: false,
  //     contentType: false,
  //     success: function (data) {
  //       console.log(JSON.stringify(data));
  //       filename = "res.json";
  //       $.ajax({
  //         type: "GET",
  //         url: "/api/files/download_json/",
  //         success: function (response) {
  //           var blob = new Blob([response]);
  //           var link = document.createElement("a");
  //           link.href = window.URL.createObjectURL(blob);
  //           link.download = filename;
  //           link.click();
  //           if (table) {
  //             const url = "/api/players/from_last_file/";
  //             table.ajax.url(url).load();
  //           } else {
  //             create_table();
  //           }
  //         },
  //       });
  //     },
  //     error: function (errMsg) {
  //       alert(`Ошибка при создании файла\n${JSON.stringify(errMsg)}`);
  //       console.log(JSON.stringify(errMsg));
  //     },
  //   });
  });
});