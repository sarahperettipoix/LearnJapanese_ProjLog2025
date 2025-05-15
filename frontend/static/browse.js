/* https://www.youtube.com/watch?v=hBbrGFCszU4 */

/* get all dropdowns */
const dropdowns = document.querySelectorAll('.dropdown');
const boddy = document.getElementById("display_location")

/* loop elements */
dropdowns.forEach(dropdown => {
    const select = dropdown.querySelector('.select');
    const caret = dropdown.querySelector('.caret');
    const menu = dropdown.querySelector('.menu');
    const options = dropdown.querySelectorAll('.menu li');
    const selected = dropdown.querySelector('.selected');
    
    select.addEventListener('click', () =>{
        select.classList.toggle('select-clicked');
        caret.classList.toggle('caret-rotate');
        menu.classList.toggle('menu-open');
    });
    options.forEach(option => {
        option.addEventListener('click', () => {
            selected.innerText = option.innerText;


            const jsonScript = document.getElementById("data-json");
            const DATA = JSON.parse(jsonScript.textContent.trim());

            if( selected.innerText == "Hiragana"){
                boddy.innerHTML = DATA.hiragana.map(item => `
                    <div class="card">
                        <p>${item.kana}  ${item.romaji}</p>
                    </div>
                `).join("");
            }
            else if(selected.innerText == "Katakana"){
                boddy.innerHTML = DATA.katakana.map(item => `
                    <div class="card">
                        <p>${item.kana}  ${item.romaji}</p>
                    </div>
                `).join("");
            }
            else if(selected.innerText == "Kanji"){
                boddy.innerHTML = DATA.kanji.map(item => `
                    <div class="card">
                        ${item.kanji}
                        <div style="font-size: 30px"> (${item.onyomi}${item.kunyomi})</div>
                        <div style="color: darkgreen; font-style: italic; font-size: 30px">${item.meaning}</div>
                    </div>
                `).join("");
            }


            
            select.classList.remove('select-clicked');
            caret.classList.remove('caret-rotate');
            menu.classList.remove('menu-open');
            
            options.forEach(option => {
                option.classList.remove('active');
            });
            option.classList.add('active');
        });
    });
});