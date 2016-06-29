import png
#pip install pypng
fin = open('odrrere.png','rb')
image = png.Reader(fin)
chunks = []
#initially found is empty
found =[0,12,8,4,9,10,6,7,3,5,2,11,1]
curr = 3 + len(found)

for i in image.chunks():
    chunks.append(i)
for i in range(0,13):
    if i in found and i > 0:
        continue
    temp = list(chunks)
    fout = open('temp/'+str(curr)+'_'+str(i)+'.png','wb')
    for j in range(0,len(found)):
        temp[3+j] = chunks[found[j]+3]
    temp[curr]  = chunks[3+i]
    png.write_chunks(fout,temp)
    fout.close()