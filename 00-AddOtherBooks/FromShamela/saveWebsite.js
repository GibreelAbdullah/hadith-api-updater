import fetch from 'node-fetch';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

async function test() {
    let url = 'https://shamela.ws/book/'
    // 1755 ,32832,33759,783,33865 ,782,33754 ,33861 ,810 ,1198,
    let books = [291020]

    for (let book of books) {

        let res = await fetch(url + book)
        let html = await res.text()

        writeFileSync(join(__dirname, 'book-' + book + '.html'), html)
        mkdirSync(join(__dirname, book.toString()), { recursive: true })

        let breakcounter = 0

        for (let i = 1; ; i++) {

            if (breakcounter > 30)
                break

            let res = await fetch(url + book + '/' + i)

            if (res.ok) {
                let html = await res.text()
                writeFileSync(join(__dirname, book.toString(), i + '.html'), html)
                breakcounter = 0
            } else
                breakcounter++
        }
    }
}

test()