// Initialize button with user's preferred color
let content = document.getElementById("content");
let url = '';
// When the button is clicked, inject setPageBackgroundColor into current page
content.addEventListener("click", async () => {
  console.log("clicked");
  chrome.runtime.reload();
});

window.onload = async function() {
  await chrome.tabs.query({active: true, lastFocusedWindow: true}, async tabs => {
      url = tabs[0].url.split('/')[4];
      await getStats(url);
  });
};

async function getStats(url){
  var requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };

  console.log(url);

  try{
    let response = await fetch("https://nfvrttoat5.execute-api.us-west-2.amazonaws.com/ext/playlist/"+url, requestOptions);
    response = await response.json();
    console.log(response);
    let happy = response[0];
    let sad = response[1];
    let energetic = response[2];
    let chill = response[3];
    content.innerHTML = '<div class="happySad">\n' +
    '    <p style="padding:0px;margin:0 10px 0 0;">Happy</p>\n' +
    '    <div class="hsBar">\n' +
    '      <div class="Hbar" style="width: '+ happy.toString() +'%;">\n' +
    '        <p style="padding:0px;margin:0px;" id=\'happyPercent\'>'+ happy.toString() +'%</p>\n' +
    '      </div>\n' +
    '      <div class="Sbar" style="width: '+ sad.toString() +'%;">\n' +
    '        <p style="padding:0px;margin:0px;" id=\'sadPercent\'>'+ sad.toString() +'%</p>\n' +
    '      </div>\n' +
    '    </div>\n' +
    '    <p style="padding:0px;margin:0 0 0 10px;">Sad</p>\n' +
    '  </div>\n' +
    '  <div class="chillEnergetic">\n' +
    '    <p style="padding:0px;margin:0 10px 0 0;">Energetic</p>\n' +
    '    <div class="ceBar">\n' +
    '      <div class="Ebar" style="width: '+ energetic.toString() +'%;">\n' +
    '        <p style="padding:0px;margin:0px;" id=\'energeticPercent\'>'+ energetic.toString() +'%</p>\n' +
    '      </div>\n' +
    '      <div class="Cbar" style="width: '+ chill.toString() +'%;">\n' +
    '        <p style="padding:0px;margin:0px;" id=\'chillPercent\'>'+ chill.toString() +'%</p>\n' +
    '      </div>\n' +
    '    </div>\n' +
    '    <p style="padding:0px;margin:0 0 0 10px;">Chill</p>\n' +
    '  </div>'
  }
  catch(err){
    content.innerHTML = '<p>'+ JSON.stringify(err) +'</p>'
  }



}
