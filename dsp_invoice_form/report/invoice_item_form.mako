<html>
<head>

<style>
	
	.row_header
		{
		border-top-style:solid;
		border-top-width:1px;
		border-top-color:#000;
		
		border-bottom-style:solid;
		border-bottom-width:1px;
		border-bottom-color:#000;
		
		border-left-style:solid;
		border-left-width:1px;
		border-left-color:#000;
		
		border-right-style:solid;
		border-right-width:1px;
		border-right-color:#000;
		}
		
	.row_col_top_only
		{
		border-top-style:solid;
		border-top-width:1px;
		border-top-color:#000;
		}
	
	.row_col_bottom_only
		{
		border-bottom-style:solid;
		border-bottom-width:1px;
		border-bottom-color:#000;
		}
	
	.row_col_left
		{
		border-left-style:solid;
		border-left-width:1px;
		border-left-color:#000;
		
		border-right-style:solid;
		border-right-width:1px;
		border-right-color:#000;
		}

	.row_line
		{
		padding:3px;

		border-right-style:solid;
		border-right-width:1px;
		border-right-color:#000;
		vertical-align:top;
		}
		
	.row_col_right
		{
		border-right-style:solid;
		border-right-width:1px;
		border-right-color:#000;
		}
		
	.row_line_bottom
		{
		padding:1px;
		
		border-left-style:solid;
		border-left-width:1px;
		border-left-color:#000;
		
		border-right-style:solid;
		border-right-width:1px;
		border-right-color:#000;
		vertical-align:top;
		
		border-bottom-style:double;
		border-bottom-width:1px;
		border-bottom-color:#000;
		}
		
	
	.row_col_left_only
		{
		border-left-style:solid;
		border-left-width:1px;
		border-left-color:#000;
		}
		
	#row_bottom
		{
		border-bottom-style:solid;
		border-bottom-width:1px;
		border-bottom-color:#000;
		}
		
			
	

</style>

<head>
	
<body>


% for inv in objects:

<table width=100% cellscpacing="0" style="border-collapse:collapse;font-family:arial;font-size:12px";>
	<tr>
		<td class="row_col_bottom_only" style="font-family:arial;font-size:12px;font-weight:bold;" width="30%">${inv.company_id.name}</td>
		<td width="40%">&nbsp;</td>
		<td style="font-family:arial;font-size:14px;font-weight:bold;">INVOICE</td>
	</tr>
</table>

 
<table width=100% cellscpacing="0" style="border-collapse:collapse;font-family:arial;font-size:12px";>
	<tr>
		<td class="row_col_left_only" width="30%">${inv.company_id.city} ${inv.company_id.zip} ${inv.company_id.country_id.name}</td>
		<td class="row_col_left_only" width="40%">&nbsp;</td>
		<td colspan="2">&nbsp;</td>
		
	</tr>
	<tr>
		<td class="row_col_left_only">&nbsp;</td>
		<td class="row_col_left_only"width="40%" >&nbsp;</td>
		<td colspan="2">&nbsp;</td>
	</tr>
	<tr>
		<td class="row_col_left_only">Phone No.: ${inv.company_id.phone}</td>
		<td class="row_col_left_only" width="40%">&nbsp;</td>
		<td colspan="2">&nbsp;</td>
	</tr>
	<tr>
		<td class="row_col_top_only" >&nbsp;</td>
		<td width="40%">&nbsp;</td>
		<td colspan="2">&nbsp;</td>
	</tr>
	
	
	<tr>
		<td class="row_header" style="font-family:arial;font-size:12px;font-weight:bold;">Invoice To</td>
		<td width="40%">&nbsp;</td>
		<td colspan="2">&nbsp;</td>
	</tr>
	<tr>
		<td class="row_col_left_only">${inv.partner_id.name}</td>
		<td class="row_col_left_only"></td>
		<td class="row_header">Invoice No.</td>
		<td class="row_header">Date</td>
	</tr>
	
	<tr>
		<td class="row_col_left_only">${inv.partner_id.street or ''}, ${inv.partner_id.street2 or ''}</td>
		<td class="row_col_left_only">&nbsp;</td>
		<td class="row_header" style="font-family:arial;font-size:12px;text-align: center";>${inv.number or ''}</td>
		<td class="row_header" style="font-family:arial;font-size:12px;text-align: center";>${inv.date_invoice or ''}</td>
	</tr>
	
	<tr>
		<td class="row_col_left_only">${inv.partner_id.city  or ''}, ${inv.partner_id.zip  or ''} ${inv.partner_id.country_id.name  or ''}</td>
		<td class="row_col_left_only">&nbsp;</td>
		<td class="row_header">Terms</td>
		<td class="row_header">Due Date</td>
	</tr>
	
	<tr>
		<td class="row_col_left_only">&nbsp;</td>
		<td class="row_col_left_only">&nbsp;</td>
		<td class="row_header" style="font-family:arial;font-size:12px;text-align: center";>${inv.payment_term.name or ''}</td>
		<td class="row_header" style="font-family:arial;font-size:12px;text-align: center";>${inv.date_due or ''}</td>
	</tr>
	
	
</table>

<table width=100% cellscpacing="0" style="border-collapse:collapse;font-family:arial;font-size:12px";>

	<tr style="font-family:arial;font-size:12px;font-weight:bold;text-align: center";>
		<td class="row_header" width="3%">No.</td>
		<td colspan="2" class="row_header" width="40%">Description</td>
		<td class="row_header">Qty</td>
		<td colspan="2" class="row_header">Price</td>
		<td colspan="2" class="row_header">Amount</td>
	</tr>
	
	<%no = 1 %> 
	% for line in inv.invoice_line: 
		<tr>
			<td class="row_col_left" style="text-align: center">${no}.</td>
			<td colspan="2" class="row_line">${line.name}</td>
			<td class="row_line" style="text-align: right">${formatLang(int(line.quantity))} ${line.uos_id.name}</td>
			<td>${inv.currency_id.symbol or ''} </td>
			<td class="row_line" style="text-align: right">${formatLang(line.price_unit)}</td>
			<td>${inv.currency_id.symbol or ''} </td>
			<td class="row_col_right" style="text-align: right">${formatLang(line.price_subtotal)}</td>
		</tr>
		
		<%no += 1 %>
		
	% endfor
	
	<tr id="row_bottom">
		<td class="row_col_left">&nbsp;</td>
		<td colspan="2" class="row_line">&nbsp;</td>
		<td class="row_line">&nbsp;</td>
		<td >&nbsp;</td>
		<td class="row_line">&nbsp;</td>
		<td >&nbsp;</td>
		<td class="row_line">&nbsp;</td>
	</tr>
	
	<tr>
		<td colspan="2" class="row_col_left_only">Please make payment</td>
		<td colspan="4" class="row_col_right" style="font-family:arial;font-size:12px;font-weight:bold;">: ${inv.company_id.name}</td>
		<td colspan="2" class="row_col_right">&nbsp;</td>
	</tr>
	<tr>
		<td colspan="2" class="row_col_left_only">&nbsp;</td>
		<td colspan="4" class="row_col_right" style="font-family:arial;font-size:12px;font-weight:bold;">&nbsp;</td>
		<td colspan="2" class="row_col_right">&nbsp;</td>
	</tr>
	<tr>
		<td colspan="2" class="row_col_left_only">To :</td>
		<td colspan="4" class="row_col_right">&nbsp;</td>
		<td>${inv.currency_id.symbol or ''} </td>
		<td class="row_col_right" style="text-align: right">${inv.amount_total}</td>
	</tr>
	<tr>
		<td colspan="2" class="row_col_left_only">&nbsp;</td>
		<td colspan="4" class="row_col_right" style="font-family:arial;font-size:12px;font-weight:bold;">&nbsp;</td>
		<td colspan="2" class="row_col_right">&nbsp;</td>
	</tr>
	<tr id="row_bottom">
		<td colspan="2" class="row_col_left_only">${inv.partner_bank_id and inv.partner_bank_id.bank_name} Account No.</td>
		<td colspan="4" class="row_col_right" style="font-family:arial;font-size:12px;font-weight:bold;">: ${inv.partner_bank_id and inv.partner_bank_id.acc_number or ''}</td>
		<td colspan="2" class="row_col_right">&nbsp;</td>
	</tr>
	
	<tr>
		<td colspan="2" height="100">&nbsp;</td>
		<td colspan="3" style="font-family:arial;font-size:12px;font-weight:bold;">&nbsp;</td>
		<td >Prepared By,</td>
		<td colspan="2" >&nbsp;</td>
	</tr>
	
	
	

</table>


% endfor

</body>
	
</html>