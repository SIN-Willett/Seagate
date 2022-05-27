!gvar edit e6deee16-b8dc-483d-9b7f-2f31d4d348d5
<drac2>
import files

def main(args):
	if not args:
		err(f"usage: {ctx.prefix}{ctx.alias} signature")

	sign = verify_signature(args[0])

	print(f"Signature verified:", '\n', stdtitle)

	print("\n".join([f"{key}: {value}" for key, value in sign.items()]))

main(&&&)
</drac2>
&STDEMBED&
