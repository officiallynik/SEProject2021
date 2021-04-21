import { idf_data } from './idf';

const GeneratorQuery = (text: string, querySize:number = 4): string => {

    const res:Array<{word: string, score: number}> = [];
    const textArray = text.split(/[.,\/#!$%\^&\*;:{}=\-_`'"~() ]/g);
    
    console.log(textArray);
    textArray.forEach(word => {
        res.push({
            word,
            score: idf_data[word] || 0
        });
    });

    res.sort((a, b) => b.score - a.score);

    let query = ""
    for(let i = 0; i<Math.min(querySize, textArray.length); i++){
        console.log(res[i]);
        query += ` ${res[i].word}`;
    }

    return query;
}

export default GeneratorQuery;