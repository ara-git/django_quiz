
function validateForm() {
    const inputElement = document.getElementById('input_text');
    const selectedValue = inputElement.value;

    const datalistOptions = document.getElementById('all_of_pokemons').options;
    const validOptions = Array.from(datalistOptions).map(option => option.value);

    if (!validOptions.includes(selectedValue)) {
        alert('リストから選択してね！');
        return false; // 画面遷移をキャンセルする
    }

    // その他の検証処理やフォームの送信などを行う
    return true;
}