$(document).ready(function(){
  console.log('document is ready')
  // $('#inference').disabled = false;
  $('#inference').click(async function(){
    console.log('Button was clicked')
    const Player1 = $('#Player1').val();
    const Player2 = ($('#Player2').val());
    console.log(Player1)
    console.log(Player2)

    data = {
      Player1,
      Player2
    }
    console.log(data)

    const response = await $.ajax('/inference', {
      data: JSON.stringify(data),
      method: "post",
      contentType: "application/json"
    })

    const parsedResponse = JSON.parse(response);
    console.log(parsedResponse);
    const player1Data = parsedResponse[Player1];
    const player2Data = parsedResponse[Player2];
    console.log('player2', player2Data);
    // console.log(response)
    // $('#comparison').val(response)

    const comparisonTable = document.getElementById('comparison');
    comparisonTable.innerHTML = '';
    const playersRow = document.createElement('tr');
    const blankHeader = document.createElement('th');
    const p1Header = document.createElement('th');
    p1Header.innerHTML = Player1;
    const p2Header = document.createElement('th');
    p2Header.innerHTML = Player2;
    [blankHeader, p1Header, p2Header].forEach(header => {
      playersRow.appendChild(header);
    });
    comparisonTable.appendChild(playersRow);

    const rowValues = [
      { title: 'Total Games', key: 'total_games' },
      { title: 'Total Shots', key: 'total_shots' },
      { title: '2 Pt Attempts', key: '2pt_attempts' },
      { title: '2 Pt %', key: '2pt%' },
      { title: '3 Pt Attempts', key: '3pt_attempts' },
      { title: '3 Pt %', key: '3pt%' },
      { title: 'FT Attempts', key: 'FT_Attempts' },
      { title: 'FT %', key: 'FT%' },
      { title: 'Total Assists', key: 'total_assists' },
      { title: 'Total Blocks', key: 'total_blocks' },
      { title: 'Offensive Rebounds', key: 'off_rebound' },
      { title: 'Clutch', key: 'is_clutch' }

    ];

    const createRow = (value) => {
      const row = document.createElement('tr');
      const header = document.createElement('th');
      const p1Data = document.createElement('td');
      const p2Data = document.createElement('td');
      header.innerHTML = value.title;
      p1Data.innerHTML = player1Data[value.key];
      p2Data.innerHTML = player2Data[value.key];
      row.appendChild(header);
      [p1Data, p2Data].forEach(data => row.appendChild(data));
      return row;
    }
    const rows = rowValues.map(value => createRow(value));
    rows.forEach(row => comparisonTable.appendChild(row));



     })
  })
