import openpyxl,datetime,sys
src,dst,ref,url=sys.argv[1:5]
wb=openpyxl.load_workbook(src);ws=wb['Inventaire']
for r in range(2,ws.max_row+1):
  if str(ws.cell(r,1).value)==ref:
    ws.cell(r,11,'En ligne'); ws.cell(r,12,datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)); ws.cell(r,12).number_format='DD/MM/YYYY'
    c=ws.cell(r,19,"Voir l'annonce"); c.hyperlink=url; c.style='Hyperlink'
    u=ws.cell(r,21).value or ''; ws.cell(r,21,(u.replace('Publication programmée','Publiée prévu')+' | publiée '+datetime.datetime.now().strftime('%d/%m %Hh%M')).strip(' |'))
    if len(sys.argv)>5 and sys.argv[5]=='repub': ws.cell(r,17,(ws.cell(r,17).value or 0)+1)
    print('row',r)
wb['Journal'].append([datetime.datetime.now(),ref,'Publication',url])
wb.save(dst)
