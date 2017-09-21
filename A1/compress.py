import re
import argparse

def repl(matchobj):
	for k,v in mapping.iteritems():
		if matchobj.group() == '<'+k :
			return '<'+v
		elif matchobj.group() == '</'+k :
			return '</'+v
	return matchobj.group()


mapping = {'!DOCTYPE':'!DT','abbr':'ab','acronym':'ac','address':'ad','applet':'ap','area':'ar','article':'art'
,'aside':'as','audio':'au','basefont':'bf','base':'ba','bdi':'bi','bdo':'bo','big':'bg','blockquote':'bq','body':'bd',
'button':'bu','canvas':'cv','caption':'ca','center':'ce','cite':'ci','code':'cd','colgroup':'cg','datalist':'da','del':'de',
'details':'da','dfn':'df','dialog':'dg','dir':'dr','div':'dv','embed':'ed','fieldset':'fs','figure':'fi','font':'ft','footer':'fr',
'form':'fm','frame':'fe','frameset':'fa','header':'he','head':'hd','html':'hl','iframe':'ir','img':'im','input':'ip','ins':'in',
'kbd':'kb','keygen':'kg','label':'la','legend':'le','link':'ln','main':'mi','map':'mp','mark':'mk','menuitem':'mm','menu':'mn',
'meta':'mt','meter':'mr','nav':'na','noframes':'nf','nscript':'ns','object':'ob','optgroup':'og','option':'op','output':'ou',
'param':'pa','picture':'pi','pre':'pr','progress':'pg','ruby':'rb','samp':'sa','script':'sc','section':'se','select':'sl',
'small':'sm','source':'so','span':'sp','strike':'st','strong':'sn','style':'sy','sub':'su','summary':'sr','table':'ta','tbody':'tb',
'textarea':'ta','tfoot':'tf','thead':'te','time':'ti','title':'tl','track':'tk','var':'vr','video':'vd','wbr':'wb'}

parser = argparse.ArgumentParser('compress')
parser.add_argument('path',help='Path to the file that will be compressed')
parser.add_argument('compressed',help='Path to the compressed file that will be generated')
args = parser.parse_args();
p_comp = args.compressed
p_path = args.path

f = open(p_path,'r')
out=""

for line in f:
	line = re.sub('</?[A-Za-z0-9]+',repl,line)
	out+=line
f.close()
f = open(p_comp,'w')
f.write(out)
f.close()
